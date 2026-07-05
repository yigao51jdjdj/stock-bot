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
    """Telegram 通知推送"""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send(self, message: str) -> bool:
        try:
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            resp = requests.post(self.api_url, json=payload, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"Telegram 发送失败: {e}")
            return False


class DingTalkNotifier:
    """钉钉机器人通知推送"""

    def __init__(self, webhook_url: str, secret: str = None):
        self.webhook_url = webhook_url
        self.secret = secret

    def send(self, message: str) -> bool:
        try:
            payload = {
                'msgtype': 'text',
                'text': {'content': message}
            }
            resp = requests.post(self.webhook_url, json=payload, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"钉钉发送失败: {e}")
            return False


class WeChatNotifier:
    """企业微信机器人通知推送"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, message: str) -> bool:
        try:
            payload = {
                'msgtype': 'text',
                'text': {'content': message}
            }
            resp = requests.post(self.webhook_url, json=payload, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            logger.error(f"企业微信发送失败: {e}")
            return False


class EmailNotifier:
    """邮件通知推送"""

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
    def _format_volume(value):
        """格式化成交量"""
        if value is None:
            return '-'
        if value >= 1e9:
            return f"{value/1e9:.2f}B"
        elif value >= 1e6:
            return f"{value/1e6:.2f}M"
        elif value >= 1e3:
            return f"{value/1e3:.2f}K"
        else:
            return f"{value:,.0f}"

    @staticmethod
    def _format_change(change_pct):
        """格式化涨跌幅"""
        if change_pct is None:
            return '-'
        sign = '+' if change_pct >= 0 else ''
        return f"{sign}{change_pct:.2f}%"

    @staticmethod
    def format_price_alert(stock_data: Dict[str, Dict]) -> str:
        """格式化价格提醒消息"""
        lines = []
        lines.append("📊 股票行情提醒")
        lines.append("=" * 55)
        lines.append("")

        for symbol, data in stock_data.items():
            if 'currentPrice' in data and data['currentPrice']:
                price = data['currentPrice']
                change_pct = data.get('changePercent')
                volume = StockMessageFormatter._format_volume(data.get('volume'))
                high = StockMessageFormatter._format_volume(data.get('todayHigh'))
                low = StockMessageFormatter._format_volume(data.get('todayLow'))

                change_str = StockMessageFormatter._format_change(change_pct)
                lines.append(f"{symbol:6s} | {price:>10.2f} | {change_str:>10s} | Vol: {volume:>10s}")
            else:
                lines.append(f"{symbol:6s} | 数据获取失败")

        lines.append("")
        lines.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(lines)

    @staticmethod
    def format_summary(stock_data: Dict[str, Dict]) -> str:
        """格式化汇总消息"""
        lines = []
        lines.append("📈 每日股票行情汇总")
        lines.append("=" * 65)
        lines.append("")

        # 分组显示
        tech_stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META', 'INTC', 'AVGO', 'MRVL']
        semi_stocks = ['MU', 'TSM', 'COHR', 'AXTI', 'AAOI']
        other_stocks = ['JPM', 'IREN', 'RKLB', 'NBIS', 'HOOD']

        groups = [
            ("科技股", tech_stocks),
            ("半导体", semi_stocks),
            ("其他", other_stocks)
        ]

        for group_name, group_symbols in groups:
            lines.append(f"【{group_name}】")
            lines.append(f"{'代码':6s} | {'价格':>10s} | {'涨跌幅':>10s} | {'成交量':>10s} | {'今日高':>10s} | {'今日低':>10s}")
            lines.append("-" * 75)

            for sym in group_symbols:
                if sym in stock_data and 'currentPrice' in stock_data[sym]:
                    data = stock_data[sym]
                    price = data.get('currentPrice', 0)
                    change_pct = data.get('changePercent')
                    volume = StockMessageFormatter._format_volume(data.get('volume'))
                    high = StockMessageFormatter._format_volume(data.get('todayHigh'))
                    low = StockMessageFormatter._format_volume(data.get('todayLow'))
                    change_str = StockMessageFormatter._format_change(change_pct)

                    lines.append(f"{sym:6s} | {price:>10.2f} | {change_str:>10s} | {volume:>10s} | {high:>10s} | {low:>10s}")
            lines.append("")

        lines.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(lines)


class StockNotifier:
    """股票通知管理器"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.notifiers = []
        self.formatter = StockMessageFormatter()
        self._init_notifiers()

    def _init_notifiers(self):
        """初始化通知渠道"""
        # Telegram
        telegram_config = self.config.get('telegram', {})
        if telegram_config.get('enabled'):
            self.notifiers.append(
                TelegramNotifier(telegram_config['bot_token'], telegram_config['chat_id'])
            )

        # 钉钉
        dingtalk_config = self.config.get('dingtalk', {})
        if dingtalk_config.get('enabled'):
            self.notifiers.append(DingTalkNotifier(dingtalk_config['webhook_url']))

        # 企业微信
        wechat_config = self.config.get('wechat', {})
        if wechat_config.get('enabled'):
            self.notifiers.append(WeChatNotifier(wechat_config['webhook_url']))

        # 邮件
        email_config = self.config.get('email', {})
        if email_config.get('enabled'):
            self.notifiers.append(
                EmailNotifier(
                    email_config['smtp_host'],
                    email_config['smtp_port'],
                    email_config['sender'],
                    email_config['password'],
                    email_config['receiver'],
                    email_config.get('use_ssl', False)
                )
            )

    def send_price_alert(self, stock_data: Dict[str, Dict]) -> Dict[str, bool]:
        """发送价格提醒"""
        message = self.formatter.format_price_alert(stock_data)
        results = {}
        for notifier in self.notifiers:
            try:
                if isinstance(notifier, EmailNotifier):
                    results[type(notifier).__name__] = notifier.send("股票行情提醒", message)
                else:
                    results[type(notifier).__name__] = notifier.send(message)
            except Exception as e:
                results[type(notifier).__name__] = False
                logger.error(f"发送失败: {e}")
        return results

    def send_summary(self, stock_data: Dict[str, Dict]) -> Dict[str, bool]:
        """发送每日汇总"""
        message = self.formatter.format_summary(stock_data)
        results = {}
        for notifier in self.notifiers:
            try:
                if isinstance(notifier, EmailNotifier):
                    results[type(notifier).__name__] = notifier.send("每日股票行情汇总", message)
                else:
                    results[type(notifier).__name__] = notifier.send(message)
            except Exception as e:
                results[type(notifier).__name__] = False
                logger.error(f"发送失败: {e}")
        return results

    def send_custom(self, message: str) -> Dict[str, bool]:
        """发送自定义消息"""
        results = {}
        for notifier in self.notifiers:
            try:
                if isinstance(notifier, EmailNotifier):
                    results[type(notifier).__name__] = notifier.send("股票通知", message)
                else:
                    results[type(notifier).__name__] = notifier.send(message)
            except Exception as e:
                results[type(notifier).__name__] = False
                logger.error(f"发送失败: {e}")
        return results