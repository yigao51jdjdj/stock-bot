# 股票数据抓取机器人

基于 GitHub Actions 的自动化股票数据抓取机器人，支持全球市场数据。

## 功能特点

- **全球市场支持**: 美股、港股、A股等多个市场
- **定时抓取**: 通过 GitHub Actions 自动定时运行
- **多数据源**: yfinance (全球)、akshare (A股)
- **多种输出格式**: JSON、CSV
- **无需服务器**: 完全基于 GitHub Actions，零运维成本

## 项目结构

```
stock-bot/
├── .github/workflows/
│   └── stock-scrape.yml      # GitHub Actions 工作流
├── src/
│   ├── scrapers/
│   │   ├── yfinance_scraper.py    # 全球市场抓取器
│   │   └── akshare_scraper.py     # A股市场抓取器
│   └── main.py                    # 主入口
├── data/                          # 数据存储目录
├── config.json                    # 配置文件
├── requirements.txt               # Python 依赖
└── README.md
```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/stock-bot.git
cd stock-bot
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置股票代码

编辑 `config.json` 文件：

```json
{
  "global_symbols": ["AAPL", "GOOGL", "MSFT"],
  "a_share_symbols": ["600519", "000858"],
  "output_format": "json"
}
```

### 4. 本地运行测试

```bash
python src/main.py
```

### 5. 部署到 GitHub

1. 创建 GitHub 仓库
2. 推送代码到仓库
3. GitHub Actions 会自动按计划运行

## GitHub Actions 配置

### 自动运行

- **定时运行**: 每周一到周五北京时间早上 9 点 (UTC 1:00)
- **手动触发**: 在 GitHub Actions 页面手动运行

### 手动触发参数

- `symbols`: 股票代码 (逗号分隔)
- `output_format`: 输出格式 (json/csv)

### 查看运行结果

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 查看最新的工作流运行
4. 下载 "stock-data" 制品查看数据

## 数据说明

### 全球市场数据 (yfinance)

- **实时价格**: 当前价格、市值、货币等
- **历史K线**: 日K、周K、月K数据
- **财务数据**: 财务报表、资产负债表
- **新闻**: 相关新闻资讯

### A股市场数据 (akshare)

- **实时行情**: A股实时价格
- **历史K线**: A股历史数据
- **市场概览**: 上证、深证、创业板指数
- **龙虎榜**: 热门股票数据

## 自定义配置

### 添加更多股票

编辑 `config.json`，添加更多股票代码：

```json
{
  "global_symbols": ["AAPL", "GOOGL", "MSFT", "NVDA", "META"],
  "a_share_symbols": ["600519", "000858", "300750", "601318"]
}
```

### 修改运行频率

编辑 `.github/workflows/stock-scrape.yml`：

```yaml
schedule:
  - cron: '0 1 * * 1-5'  # 修改为你需要的时间
```

## 数据存储

### GitHub Artifacts

- 数据会自动上传为 GitHub Artifacts
- 保留 30 天
- 可在 Actions 页面下载

### Git 提交

- 工作流会自动提交数据到 `data/` 目录
- 每次运行会创建新的数据文件
- 文件名包含时间戳，便于管理

## 常见问题

### Q: 为什么选择 GitHub Actions？

A: 免费、无需服务器、自动运行、易于维护。

### Q: 数据抓取失败怎么办？

A: 检查 Actions 日志，可能是网络问题或 API 限制。

### Q: 如何添加更多数据源？

A: 在 `src/scrapers/` 目录下创建新的抓取器模块。

### Q: 数据格式可以自定义吗？

A: 可以修改 `src/main.py` 中的 `_save_data` 方法。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License