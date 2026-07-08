"""
股票数据通知推送模块
支持: Telegram、钉钉、邮件、企业微信
"""

import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send(self, message: str) -> bool:
        try:
            payload = {'chat_id': self.chat_id, 'text': message, 'parse_mode': 'HTML'}
            resp = requests.post(self.api_url, json=payload, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"Telegram 发送失败: {e}")
            return False


class DingTalkNotifier:
    def __init__(self, webhook_url: str, secret: str = None):
        self.webhook_url = webhook_url

    def send(self, message: str) -> bool:
        try:
            payload = {'msgtype': 'text', 'text': {'content': message}}
            resp = requests.post(self.webhook_url, json=payload, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"钉钉发送失败: {e}")
            return False


class WeChatNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, message: str) -> bool:
        try:
            payload = {'msgtype': 'text', 'text': {'content': message}}
            resp = requests.post(self.webhook_url, json=payload, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"企业微信发送失败: {e}")
            return False


class EmailNotifier:
    def __init__(self, smtp_host: str, smtp_port: int, sender: str, password: str, receiver: str, use_ssl: bool = False):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender = sender
        self.password = password
        self.receiver = receiver
        self.use_ssl = use_ssl

    def send(self, subject: str, message: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = self.receiver
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain', 'utf-8'))

            if self.use_ssl:
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, timeout=10) as server:
                    server.login(self.sender, self.password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                    server.starttls()
                    server.login(self.sender, self.password)
                    server.send_message(msg)
            return True
        except Exception as e:
            logger.error(f"邮件发送失败: {e}")
            return False


class StockMessageFormatter:
    """股票消息格式化"""

    @staticmethod
    def _fmt_vol(v):
        if v is None: return '-'
        if v >= 1e9: return f"{v/1e9:.1f}B"
        if v >= 1e6: return f"{v/1e6:.1f}M"
        if v >= 1e3: return f"{v/1e3:.1f}K"
        return str(int(v))

    @staticmethod
    def _fmt_chg(c):
        if c is None: return '-'
        return f"+{c:.2f}%" if c >= 0 else f"{c:.2f}%"

    @staticmethod
    def format_summary(stock_data: Dict[str, Dict]) -> str:
        """格式化汇总消息"""
        lines = []
        lines.append("📈 股票行情")
        lines.append("=" * 50)
        lines.append("")

        # 分组
        index_etf = ['QQQ', 'SPY', 'GLD', 'EWJ']
        crypto_ai = ['MSTR', 'IREN']
        semi = ['NVDA', 'AVGO', 'MRVL', 'MU', 'TSM', 'COHR', 'AXTI', 'AAOI', 'NBIS']
        intl = ['005930.KS', 'SKHY']
        other = ['SNDK', 'CRCL', 'CCXI', 'JPM', 'RKLB', 'HOOD']

        groups = [("指数/ETF", index_etf), ("加密/AI", crypto_ai), ("半导体", semi), ("国际", intl), ("其他", other)]

        lines.append(f"{'代码':10s} | {'价格':>10s} | {'涨跌':>8s}")
        lines.append("-" * 35)

        for name, syms in groups:
            lines.append(f"【{name}】")
            for sym in syms:
                if sym in stock_data and 'currentPrice' in stock_data[sym]:
                    d = stock_data[sym]
                    p = d.get('currentPrice')
                    c = StockMessageFormatter._fmt_chg(d.get('changePercent'))
                    if p is not None:
                        lines.append(f"{sym:10s} | ${p:>9.2f} | {c:>8s}")
                    else:
                        lines.append(f"{sym:10s} | {'-':>10s} | {c:>8s}")
            lines.append("")

        lines.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        return "\n".join(lines)


class StockNotifier:
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.notifiers = []
        self.formatter = StockMessageFormatter()
        self._init_notifiers()

    def _init_notifiers(self):
        telegram_config = self.config.get('telegram', {})
        if telegram_config.get('enabled'):
            self.notifiers.append(TelegramNotifier(telegram_config['bot_token'], telegram_config['chat_id']))

        dingtalk_config = self.config.get('dingtalk', {})
        if dingtalk_config.get('enabled'):
            self.notifiers.append(DingTalkNotifier(dingtalk_config['webhook_url']))

        wechat_config = self.config.get('wechat', {})
        if wechat_config.get('enabled'):
            self.notifiers.append(WeChatNotifier(wechat_config['webhook_url']))

        email_config = self.config.get('email', {})
        if email_config.get('enabled'):
            self.notifiers.append(EmailNotifier(
                email_config['smtp_host'], email_config['smtp_port'],
                email_config['sender'], email_config['password'],
                email_config['receiver'], email_config.get('use_ssl', False)
            ))

    def send_summary(self, stock_data: Dict[str, Dict]) -> Dict[str, bool]:
        message = self.formatter.format_summary(stock_data)
        results = {}
        for notifier in self.notifiers:
            try:
                if isinstance(notifier, EmailNotifier):
                    results[type(notifier).__name__] = notifier.send("每日股票行情", message)
                else:
                    results[type(notifier).__name__] = notifier.send(message)
            except Exception as e:
                results[type(notifier).__name__] = False
                logger.error(f"发送失败: {e}")
        return results

    def send_price_alert(self, stock_data: Dict[str, Dict]) -> Dict[str, bool]:
        return self.send_summary(stock_data)

    def send_custom(self, message: str) -> Dict[str, bool]:
        results = {}
        for notifier in self.notifiers:
            try:
                if isinstance(notifier, EmailNotifier):
                    results[type(notifier).__name__] = notifier.send("股票通知", message)
                else:
                    results[type(notifier).__name__] = notifier.send(message)
            except Exception as e:
                results[type(notifier).__name__] = False
        return results