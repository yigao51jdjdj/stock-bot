"""
全球股票数据抓取器 - 使用 Yahoo Finance API
支持: 美股、港股、全球主要市场
"""

import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import logging
import time
import re

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


class YFinanceScraper:
    """股票数据抓取器"""

    def __init__(self, symbols: List[str], delay: float = 1.0):
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
        """获取当前价格"""
        results = {}
        for i, symbol in enumerate(self.symbols):
            try:
                url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
                params = {'interval': '1d', 'range': '5d'}
                data = self._request(url, params)

                if 'chart' in data and data['chart']['result']:
                    meta = data['chart']['result'][0]['meta']
                    current_price = meta.get('regularMarketPrice')
                    previous_close = meta.get('previousClose') or meta.get('chartPreviousClose')

                    change_pct = None
                    if current_price and previous_close and previous_close > 0:
                        change_pct = ((current_price - previous_close) / previous_close) * 100

                    # 从历史数据中提取更多信息
                    result = data['chart']['result'][0]
                    indicators = result.get('indicators', {}).get('quote', [{}])[0]

                    # 获取今日数据
                    volumes = indicators.get('volume', [])
                    highs = indicators.get('high', [])
                    lows = indicators.get('low', [])

                    today_volume = volumes[-1] if volumes else None
                    today_high = highs[-1] if highs else None
                    today_low = lows[-1] if lows else None

                    # 计算52周高低（从历史数据推断）
                    all_highs = [h for h in highs if h is not None]
                    all_lows = [l for l in lows if l is not None]

                    results[symbol] = {
                        'symbol': symbol,
                        'name': meta.get('shortName', symbol),
                        'currentPrice': current_price,
                        'previousClose': previous_close,
                        'changePercent': round(change_pct, 2) if change_pct else None,
                        'currency': meta.get('currency', 'USD'),
                        'exchange': meta.get('exchangeName', ''),
                        'todayHigh': today_high,
                        'todayLow': today_low,
                        'volume': today_volume,
                        'periodHigh': max(all_highs) if all_highs else None,
                        'periodLow': min(all_lows) if all_lows else None,
                        'timestamp': datetime.now().isoformat()
                    }
                    logger.info(f"[{i+1}/{len(self.symbols)}] {symbol}: {current_price}")

            except Exception as e:
                logger.error(f"获取 {symbol} 当前价格失败: {e}")
                results[symbol] = {'error': str(e)}

            if i < len(self.symbols) - 1:
                time.sleep(self.delay)

        return results

    def fetch_historical_data(self, period: str = "1mo", interval: str = "1d") -> Dict[str, pd.DataFrame]:
        """获取历史数据"""
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

            except Exception as e:
                logger.error(f"获取 {symbol} 历史数据失败: {e}")

            if i < len(self.symbols) - 1:
                time.sleep(self.delay)

        return results


def get_global_market_data(symbols: List[str]) -> Dict:
    """获取全球市场数据的便捷函数"""
    scraper = YFinanceScraper(symbols, delay=1.0)

    return {
        'current': scraper.fetch_current_price(),
        'historical': scraper.fetch_historical_data(period="1mo"),
        'timestamp': datetime.now().isoformat()
    }