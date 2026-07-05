"""
全球股票数据抓取器 - 使用 Yahoo Finance 直接 API
支持: 美股、港股、全球主要市场
"""

import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import logging
import time

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


class YFinanceScraper:
    """Yahoo Finance API 数据抓取器"""

    def __init__(self, symbols: List[str], delay: float = 1.0):
        """
        初始化抓取器
        Args:
            symbols: 股票代码列表，如 ['AAPL', '00700.HK', '600519.SS']
            delay: 请求间隔（秒），避免被限流
        """
        self.symbols = symbols
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _request(self, url: str, params: dict = None) -> dict:
        """发送请求并处理错误"""
        try:
            resp = self.session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {e}")
            return {}

    def fetch_current_price(self) -> Dict[str, Dict]:
        """获取当前价格信息"""
        results = {}
        for i, symbol in enumerate(self.symbols):
            try:
                url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
                params = {'interval': '1d', 'range': '1d'}
                data = self._request(url, params)

                if 'chart' in data and data['chart']['result']:
                    meta = data['chart']['result'][0]['meta']
                    results[symbol] = {
                        'symbol': symbol,
                        'name': meta.get('shortName', symbol),
                        'currentPrice': meta.get('regularMarketPrice'),
                        'previousClose': meta.get('previousClose'),
                        'currency': meta.get('currency', 'USD'),
                        'exchange': meta.get('exchangeName', ''),
                        'marketCap': meta.get('marketCap'),
                        'timestamp': datetime.now().isoformat()
                    }
                    price = meta.get('regularMarketPrice', 'N/A')
                    logger.info(f"[{i+1}/{len(self.symbols)}] {symbol}: {price}")
                else:
                    results[symbol] = {'error': 'No data available'}
                    logger.warning(f"[{i+1}/{len(self.symbols)}] {symbol}: 无数据")

            except Exception as e:
                logger.error(f"获取 {symbol} 当前价格失败: {e}")
                results[symbol] = {'error': str(e)}

            if i < len(self.symbols) - 1:
                time.sleep(self.delay)

        return results

    def fetch_historical_data(self, period: str = "1mo", interval: str = "1d") -> Dict[str, pd.DataFrame]:
        """
        获取历史数据
        Args:
            period: 数据周期 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: 数据间隔 (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        """
        results = {}
        for i, symbol in enumerate(self.symbols):
            try:
                url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
                params = {'interval': interval, 'range': period}
                data = self._request(url, params)

                if 'chart' in data and data['chart']['result']:
                    result = data['chart']['result'][0]
                    timestamps = result['timestamp']
                    quotes = result['indicators']['quote'][0]

                    df = pd.DataFrame({
                        'Date': pd.to_datetime(timestamps, unit='s'),
                        'Open': quotes.get('open', []),
                        'High': quotes.get('high', []),
                        'Low': quotes.get('low', []),
                        'Close': quotes.get('close', []),
                        'Volume': quotes.get('volume', [])
                    })
                    df.set_index('Date', inplace=True)
                    results[symbol] = df
                    logger.info(f"[{i+1}/{len(self.symbols)}] {symbol}: {len(df)} 条历史记录")
                else:
                    logger.warning(f"[{i+1}/{len(self.symbols)}] {symbol}: 无历史数据")

            except Exception as e:
                logger.error(f"获取 {symbol} 历史数据失败: {e}")

            if i < len(self.symbols) - 1:
                time.sleep(self.delay)

        return results

    def fetch_news(self, max_news: int = 5) -> Dict[str, List[Dict]]:
        """获取股票相关新闻"""
        results = {}
        for i, symbol in enumerate(self.symbols):
            try:
                url = f'https://query1.finance.yahoo.com/v1/finance/search'
                params = {'q': symbol, 'newsCount': max_news}
                data = self._request(url, params)

                news = data.get('news', [])
                results[symbol] = [
                    {
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'publisher': item.get('publisher', ''),
                        'providerPublishTime': item.get('providerPublishTime')
                    }
                    for item in news[:max_news]
                ]
                logger.info(f"[{i+1}/{len(self.symbols)}] {symbol}: {len(news)} 条新闻")

            except Exception as e:
                logger.error(f"获取 {symbol} 新闻失败: {e}")
                results[symbol] = []

            if i < len(self.symbols) - 1:
                time.sleep(self.delay)

        return results


def get_global_market_data(symbols: List[str]) -> Dict:
    """获取全球市场数据的便捷函数"""
    scraper = YFinanceScraper(symbols, delay=1.0)

    return {
        'current': scraper.fetch_current_price(),
        'historical': scraper.fetch_historical_data(period="1mo"),
        'news': scraper.fetch_news(),
        'timestamp': datetime.now().isoformat()
    }