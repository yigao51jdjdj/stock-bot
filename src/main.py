"""
股票数据抓取机器人 - 主入口
支持全球市场数据抓取、存储和通知推送
"""

import os
import json
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional
import logging
import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 添加项目根目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scrapers.yfinance_scraper import YFinanceScraper, get_global_market_data
from scrapers.akshare_scraper import AkShareScraper, get_a_share_data
from notifiers.notifier import StockNotifier


class StockDataBot:
    """股票数据抓取机器人"""

    def __init__(self, config_path: str = None):
        """
        初始化机器人
        Args:
            config_path: 配置文件路径，默认为 config.json
        """
        self.config = self._load_config(config_path)
        self.data_dir = Path(self.config.get('data_dir', 'data'))
        self.data_dir.mkdir(exist_ok=True)

        # 初始化抓取器
        self.global_scraper = YFinanceScraper(
            self.config.get('global_symbols', []),
            delay=1.0
        )
        self.a_share_scraper = AkShareScraper(
            self.config.get('a_share_symbols', [])
        )

        # 初始化通知器
        self.notifier = StockNotifier(self.config.get('notifications', {}))

    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        default_config = {
            'global_symbols': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'],
            'a_share_symbols': ['600519', '000858', '300750'],
            'data_dir': 'data',
            'output_format': 'json',
            'fetch_historical_days': 30,
            'notifications': {}
        }

        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def run(self, notify: bool = True, notify_type: str = 'summary'):
        """
        执行数据抓取任务
        Args:
            notify: 是否发送通知
            notify_type: 通知类型 ('price' 或 'summary')
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        logger.info("开始抓取数据 - {}".format(timestamp))

        results = {
            'timestamp': timestamp,
            'global_market': {},
            'a_share_market': {},
            'status': 'success'
        }

        try:
            # 抓取全球市场数据
            logger.info("抓取全球市场数据...")
            results['global_market'] = get_global_market_data(
                self.config.get('global_symbols', [])
            )

            # 抓取A股市场数据
            logger.info("抓取A股市场数据...")
            try:
                results['a_share_market'] = get_a_share_data(
                    self.config.get('a_share_symbols', [])
                )
            except Exception as e:
                logger.warning("A股数据抓取失败: {}".format(e))
                results['a_share_market'] = {'error': str(e)}

            # 保存数据
            self._save_data(results, timestamp)
            logger.info("数据抓取完成并保存 - {}".format(timestamp))

            # 发送通知
            if notify and self.notifier.notifiers:
                logger.info("发送通知...")
                stock_data = results['global_market'].get('current', {})
                if notify_type == 'price':
                    notify_results = self.notifier.send_price_alert(stock_data)
                else:
                    notify_results = self.notifier.send_summary(stock_data)
                results['notification'] = notify_results
                logger.info("通知发送结果: {}".format(notify_results))

        except Exception as e:
            logger.error("数据抓取失败: {}".format(e))
            results['status'] = 'failed'
            results['error'] = str(e)

        return results

    def _save_data(self, data: dict, timestamp: str):
        """保存数据到文件"""
        format_type = self.config.get('output_format', 'json')

        if format_type == 'json':
            file_path = self.data_dir / 'stock_data_{}.json'.format(timestamp)
            serializable_data = self._prepare_for_json(data)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, ensure_ascii=False, indent=2)

        elif format_type == 'csv':
            if 'global_market' in data and 'historical' in data['global_market']:
                for symbol, df in data['global_market']['historical'].items():
                    if hasattr(df, 'to_csv'):
                        csv_path = self.data_dir / 'global_{}_{}.csv'.format(symbol, timestamp)
                        df.to_csv(csv_path)

            if 'a_share_market' in data:
                if 'realtime' in data['a_share_market'] and hasattr(data['a_share_market']['realtime'], 'to_csv'):
                    csv_path = self.data_dir / 'a_share_realtime_{}.csv'.format(timestamp)
                    data['a_share_market']['realtime'].to_csv(csv_path)

        logger.info("数据已保存到 {}".format(self.data_dir))

    def _prepare_for_json(self, obj):
        """递归转换对象为 JSON 可序列化格式"""
        if isinstance(obj, dict):
            return {str(k): self._prepare_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._prepare_for_json(item) for item in obj]
        elif isinstance(obj, pd.DataFrame):
            # 将 DataFrame 转换为字典列表
            return self._prepare_for_json(obj.to_dict('records'))
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif hasattr(obj, 'item'):
            return obj.item()
        return obj


def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description='股票数据抓取机器人')
    parser.add_argument('--config', '-c', type=str, help='配置文件路径')
    parser.add_argument('--output', '-o', type=str, choices=['json', 'csv'],
                       default='json', help='输出格式')
    parser.add_argument('--no-notify', action='store_true', help='不发送通知')
    parser.add_argument('--notify-type', type=str, choices=['price', 'summary'],
                       default='summary', help='通知类型')

    args = parser.parse_args()

    # 创建机器人实例
    bot = StockDataBot(config_path=args.config)

    # 执行抓取
    results = bot.run(notify=not args.no_notify, notify_type=args.notify_type)

    # 打印摘要
    print("\n" + "=" * 50)
    print("抓取结果摘要")
    print("=" * 50)
    print("状态: {}".format(results.get('status', 'unknown')))
    print("时间: {}".format(results.get('timestamp', 'unknown')))

    if 'global_market' in results:
        current = results['global_market'].get('current', {})
        print("\n全球市场数据: {} 只股票".format(len(current)))
        for symbol, data in current.items():
            if 'currentPrice' in data:
                print("  {}: {} {}".format(symbol, data['currentPrice'], data.get('currency', 'USD')))

    if 'a_share_market' in results:
        realtime = results['a_share_market'].get('realtime')
        if realtime is not None and hasattr(realtime, 'shape'):
            print("\nA股市场数据: {} 只股票".format(realtime.shape[0]))

    if 'notification' in results:
        print("\n通知发送结果:")
        for channel, success in results['notification'].items():
            print("  {}: {}".format(channel, '成功' if success else '失败'))

    print("=" * 50)


if __name__ == "__main__":
    main()