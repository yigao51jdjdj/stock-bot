"""
A股市场数据抓取器 - 使用 akshare
支持: A股实时行情、历史K线、财务数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class AkShareScraper:
    """akshare A股数据抓取器"""

    def __init__(self, symbols: List[str] = None):
        """
        初始化抓取器
        Args:
            symbols: A股代码列表，如 ['600519', '000858', '300750']
        """
        self.symbols = symbols or []

    def fetch_realtime_quote(self) -> pd.DataFrame:
        """获取A股实时行情"""
        try:
            df = ak.stock_zh_a_spot_em()
            logger.info(f"获取A股实时行情: {len(df)} 只股票")
            return df
        except Exception as e:
            logger.error(f"获取A股实时行情失败: {e}")
            return pd.DataFrame()

    def fetch_stock_history(self, symbol: str, period: str = "daily",
                           start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        获取单只股票历史K线
        Args:
            symbol: 股票代码，如 '600519'
            period: 周期 (daily, weekly, monthly)
            start_date: 开始日期 (YYYYMMDD)
            end_date: 结束日期 (YYYYMMDD)
        """
        try:
            if not start_date:
                start_date = (datetime.now() - pd.Timedelta(days=30)).strftime('%Y%m%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"  # 前复权
            )
            logger.info(f"获取 {symbol} 历史数据: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"获取 {symbol} 历史数据失败: {e}")
            return pd.DataFrame()

    def fetch_stock_info(self, symbol: str) -> Dict:
        """获取单只股票基本信息"""
        try:
            info = ak.stock_individual_info_em(symbol=symbol)
            return info.to_dict('records')[0] if not info.empty else {}
        except Exception as e:
            logger.error(f"获取 {symbol} 基本信息失败: {e}")
            return {}

    def fetch_financial_report(self, symbol: str, report_type: str = "income") -> pd.DataFrame:
        """
        获取财务报表
        Args:
            symbol: 股票代码
            report_type: 报表类型 (income/balance/cashflow)
        """
        try:
            if report_type == "income":
                df = ak.stock_profit_sheet_by_report_em(symbol=symbol)
            elif report_type == "balance":
                df = ak.stock_balance_sheet_by_report_em(symbol=symbol)
            elif report_type == "cashflow":
                df = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
            else:
                raise ValueError(f"不支持的报表类型: {report_type}")
            
            logger.info(f"获取 {symbol} {report_type} 报表: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"获取 {symbol} {report_type} 报表失败: {e}")
            return pd.DataFrame()

    def fetch_market_overview(self) -> Dict:
        """获取A股市场概览"""
        try:
            # 上证指数
            sh_index = ak.stock_zh_index_daily(symbol="sh000001")
            # 深证成指
            sz_index = ak.stock_zh_index_daily(symbol="sz399001")
            # 创业板指
            cy_index = ak.stock_zh_index_daily(symbol="sz399006")
            
            return {
                '上证指数': sh_index.tail(1).to_dict('records')[0],
                '深证成指': sz_index.tail(1).to_dict('records')[0],
                '创业板指': cy_index.tail(1).to_dict('records')[0],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取市场概览失败: {e}")
            return {}

    def fetch_hot_stocks(self) -> pd.DataFrame:
        """获取热门股票（龙虎榜）"""
        try:
            df = ak.stock_lhb_detail_em()
            logger.info(f"获取龙虎榜数据: {len(df)} 条记录")
            return df
        except Exception as e:
            logger.error(f"获取龙虎榜数据失败: {e}")
            return pd.DataFrame()


def get_a_share_data(symbols: List[str] = None) -> Dict:
    """
    获取A股数据的便捷函数
    """
    scraper = AkShareScraper(symbols)
    
    result = {
        'realtime': scraper.fetch_realtime_quote(),
        'marketOverview': scraper.fetch_market_overview(),
        'hotStocks': scraper.fetch_hot_stocks(),
        'timestamp': datetime.now().isoformat()
    }
    
    # 获取指定股票的历史数据
    if symbols:
        history = {}
        for symbol in symbols:
            history[symbol] = scraper.fetch_stock_history(symbol)
        result['history'] = history
    
    return result