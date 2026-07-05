# 快速开始指南

## 🚀 5分钟快速部署

### 第一步：安装依赖

```bash
# Windows 用户
双击运行 run.bat

# 或者使用命令行
pip install -r requirements.txt
```

### 第二步：配置股票代码

编辑 `config.json` 文件：

```json
{
  "global_symbols": ["AAPL", "GOOGL", "MSFT"],
  "a_share_symbols": ["600519", "000858"]
}
```

### 第三步：本地测试

```bash
python test_scraper.py
```

### 第四步：运行抓取

```bash
python src/main.py
```

## 📊 数据源配置

### 全球市场 (yfinance)

支持的股票代码格式：
- 美股：`AAPL`, `GOOGL`, `MSFT`
- 港股：`00700.HK`
- 其他：`600519.SS` (上海), `600519.SZ` (深圳)

### A股市场 (akshare)

支持的股票代码格式：
- 上海：`600519`
- 深圳：`000858`, `300750`

## ⏰ GitHub Actions 部署

### 1. 创建 GitHub 仓库

```bash
git init
git add .
git commit -m "Initial commit: Stock data bot"
git remote add origin https://github.com/yourusername/stock-bot.git
git push -u origin main
```

### 2. 启用 GitHub Actions

- 进入 GitHub 仓库
- 点击 "Actions" 标签
- 点击 "I understand my workflows, go ahead and enable them"

### 3. 手动触发测试

- 进入 "Actions" -> "Stock Data Scraper"
- 点击 "Run workflow"
- 等待运行完成
- 下载 "stock-data" 制品

## 📁 数据输出

### JSON 格式

```json
{
  "timestamp": "20240115_090000",
  "global_market": {
    "current": {
      "AAPL": {
        "currentPrice": 185.50,
        "currency": "USD",
        "marketCap": 2850000000000
      }
    },
    "historical": {...}
  },
  "a_share_market": {...}
}
```

### CSV 格式

- `global_AAPL_20240115_090000.csv`
- `a_share_realtime_20240115_090000.csv`

## 🔧 自定义配置

### 修改运行频率

编辑 `.github/workflows/stock-scrape.yml`：

```yaml
schedule:
  - cron: '0 1 * * 1-5'  # 每周一到周五 UTC 1:00 (北京时间 9:00)
```

### 添加更多股票

编辑 `config.json`：

```json
{
  "global_symbols": [
    "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA",
    "NVDA", "META", "JPM", "V", "JNJ"
  ],
  "a_share_symbols": [
    "600519", "000858", "300750", "601318",
    "000001", "600036", "601166"
  ]
}
```

## ❓ 常见问题

### Q: 网络连接失败怎么办？

A: 检查网络连接，可能需要配置代理：
```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
```

### Q: 如何查看运行日志？

A: 在 GitHub Actions 页面点击具体的运行记录查看详细日志。

### Q: 数据如何下载？

A: 两种方式：
1. GitHub Actions 页面下载 Artifacts
2. 克隆仓库查看 `data/` 目录

### Q: 如何添加更多数据源？

A: 在 `src/scrapers/` 目录创建新的抓取器模块，参考现有实现。

## 📞 获取帮助

- 查看 README.md 了解详细文档
- 查看源代码注释
- 提交 GitHub Issue