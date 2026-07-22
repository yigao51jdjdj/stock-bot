"""
全球股票数据抓取器 - 多数据源支持
主要数据源: 新浪财经 (稳定、免费、国内友好)
备选数据源: yfinance
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List
import logging
import time
import requests
import re

logger = logging.getLogger(__name__)


class SinaScraper:
    """新浪财经数据抓取器"""

    def __init__(self, symbols: List[str]):
        self.symbols = symbols
        self.session = requests.Session()
        self.session.headers.update({
            'Referer': 'https://finance.sina.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def _convert_symbol(self, symbol: str) -> str:
        """转换股票代码为新浪格式"""
        symbol = symbol.upper()

        # 港股 (5位数字)
        if re.match(r'^\d{5}$', symbol):
            return f'hk_{symbol}'

        # A股
        if symbol.startswith('6') or symbol.startswith('9'):
            return f'sh_{symbol}'
        elif symbol.startswith('0') or symbol.startswith('3'):
            return f'sz_{symbol}'

        # 美股
        return f'gb_{symbol.lower()}'

    def fetch_current_price(self) -> Dict[str, Dict]:
        """获取当前价格"""
        results = {}
        sina_symbols = [self._convert_symbol(s) for s in self.symbols]
        symbols_str = ','.join(sina_symbols)

        try:
            url = f'https://hq.sinajs.cn/list={symbols_str}'
            resp = self.session.get(url, timeout=15)
            resp.encoding = 'gbk'

            lines = resp.text.strip().split('\n')

            for i, line in enumerate(lines):
                if i >= len(self.symbols):
                    break

                symbol = self.symbols[i]
                try:
                    match = re.search(r'"([^"]*)"', line)
                    if not match:
                        continue

                    data_str = match.group(1)
                    if not data_str:
                        continue

                    parts = data_str.split(',')
                    sina_symbol = sina_symbols[i]

                    if sina_symbol.startswith('gb_'):
                        # 美股: 名称,当前价,涨跌额,涨跌幅,...
                        if len(parts) < 4:
                            continue
                        name = parts[0]
                        current_price = float(parts[1]) if parts[1] else None
                        change_pct = float(parts[2]) if parts[2] else None

                    elif sina_symbol.startswith('hk_'):
                        # 港股
                        if len(parts) < 7:
                            continue
                        name = parts[1]
                        current_price = float(parts[6]) if parts[6] else None
                        change_pct = float(parts[3]) if parts[3] else None

                    else:
                        # A股
                        if len(parts) < 4:
                            continue
                        name = parts[0]
                        current_price = float(parts[3]) if parts[3] else None
                        prev_close = float(parts[2]) if parts[2] else None
                        if current_price and prev_close and prev_close > 0:
                            change_pct = ((current_price - prev_close) / prev_close) * 100
                        else:
                            change_pct = None

                    if current_price and current_price > 0:
                        currency = 'USD' if sina_symbol.startswith('gb_') else ('HKD' if sina_symbol.startswith('hk_') else 'CNY')
                        results[symbol] = {
                            'symbol': symbol,
                            'name': name,
                            'currentPrice': current_price,
                            'changePercent': round(change_pct, 2) if change_pct else None,
                            'currency': currency,
                            'source': 'sina',
                            'timestamp': datetime.now().isoformat()
                        }
                        logger.info(f"  {symbol}: {current_price:.2f}")

                except Exception as e:
                    logger.debug(f"解析 {symbol} 数据失败: {e}")

        except Exception as e:
            logger.error(f"新浪数据获取失败: {e}")

        return results


class YFinanceScraper:
    """股票数据抓取器"""

    def __init__(self, symbols: List[str], delay: float = 2.0):
        self.symbols = symbols
        self.delay = delay
        self.sina = SinaScraper(symbols)

    def fetch_current_price(self) -> Dict[str, Dict]:
        """获取当前价格 - 优先使用新浪"""
        logger.info("从新浪获取美股数据...")
        results = self.sina.fetch_current_price()

        failed = [s for s in self.symbols if s not in results]
        if failed:
            logger.info(f"新浪未获取到 {len(failed)} 只，尝试 yfinance...")
            try:
                import yfinance as yf
                for symbol in failed:
                    try:
                        ticker = yf.Ticker(symbol)
                        hist = ticker.history(period="2d")
                        if not hist.empty:
                            current_price = hist['Close'].iloc[-1]
                            change_pct = None
                            if len(hist) >= 2:
                                prev = hist['Close'].iloc[-2]
                                if prev > 0:
                                    change_pct = ((current_price - prev) / prev) * 100
                            results[symbol] = {
                                'symbol': symbol,
                                'currentPrice': float(current_price),
                                'changePercent': round(change_pct, 2) if change_pct else None,
                                'currency': 'USD',
                                'source': 'yfinance',
                                'timestamp': datetime.now().isoformat()
                            }
                            logger.info(f"  {symbol}: {current_price:.2f} (yfinance)")
                    except Exception as e:
                        logger.error(f"  {symbol}: {e}")
                    time.sleep(self.delay)
            except ImportError:
                logger.warning("yfinance 未安装")

        return results

    def fetch_historical_data(self, period: str = "1mo", interval: str = "1d") -> Dict[str, pd.DataFrame]:
        """获取历史数据"""
        results = {}

        # 尝试从新浪获取
        try:
            for symbol in self.symbols:
                try:
                    sina_symbol = self.sina._convert_symbol(symbol)
                    url = 'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData'
                    params = {
                        'symbol': sina_symbol,
                        'scale': '240',
                        'ma': 'no',
                        'datalen': '30'
                    }
                    resp = self.sina.session.get(url, params=params, timeout=10)
                    if resp.status_code == 200:
                        data = resp.json()
                        if data:
                            df = pd.DataFrame(data)
                            df['Date'] = pd.to_datetime(df['day'])
                            df = df.set_index('Date')
                            df = df[['open', 'high', 'low', 'close', 'volume']].rename(
                                columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}
                            )
                            df = df.astype(float)
                            results[symbol] = df
                            logger.info(f"  {symbol}: {len(df)} 条历史记录")
                except Exception as e:
                    logger.debug(f"获取 {symbol} 历史数据失败: {e}")
                time.sleep(0.3)
        except Exception as e:
            logger.error(f"新浪历史数据获取失败: {e}")

        # 尝试从 yfinance 获取缺失的
        failed = [s for s in self.symbols if s not in results]
        if failed:
            logger.info(f"尝试从 yfinance 获取 {len(failed)} 只历史数据...")
            try:
                import yfinance as yf
                for symbol in failed:
                    try:
                        ticker = yf.Ticker(symbol)
                        df = ticker.history(period=period, interval=interval)
                        if not df.empty:
                            results[symbol] = df[['Open', 'High', 'Low', 'Close', 'Volume']]
                            logger.info(f"  {symbol}: {len(df)} 条历史记录 (yfinance)")
                    except Exception as e:
                        logger.debug(f"  {symbol} 失败: {e}")
                    time.sleep(self.delay)
            except ImportError:
                pass

        return results


def get_global_market_data(symbols: List[str]) -> Dict:
    """获取全球市场数据的便捷函数"""
    scraper = YFinanceScraper(symbols, delay=2.0)

    return {
        'current': scraper.fetch_current_price(),
        'historical': scraper.fetch_historical_data(period="1mo"),
        'timestamp': datetime.now().isoformat()
    }
