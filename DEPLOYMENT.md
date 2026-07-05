# 部署指南

本指南将帮助你部署股票数据抓取机器人到不同的平台。

## 🚀 方式一：GitHub Actions（推荐）

这是最简单的部署方式，无需服务器。

### 步骤

1. **创建 GitHub 仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/stock-bot.git
   git push -u origin main
   ```

2. **启用 GitHub Actions**
   - 进入仓库页面
   - 点击 "Actions" 标签
   - 点击 "I understand my workflows, go ahead and enable them"

3. **配置运行时间**
   编辑 `.github/workflows/stock-scrape.yml`：
   ```yaml
   schedule:
     - cron: '0 1 * * 1-5'  # 每周一到周五 UTC 1:00
   ```

4. **手动测试**
   - 点击 "Actions" -> "Stock Data Scraper"
   - 点击 "Run workflow"
   - 等待运行完成

### 优点
- ✅ 免费
- ✅ 无需服务器
- ✅ 自动运行
- ✅ 易于维护

## 🐳 方式二：Docker 部署

适合需要更灵活控制的用户。

### 使用 Docker

```bash
# 构建镜像
docker build -t stock-bot .

# 运行容器
docker run -v $(pwd)/config.json:/app/config.json -v $(pwd)/data:/app/data stock-bot
```

### 使用 Docker Compose

```bash
# 单次运行
docker-compose run stock-bot

# 启动定时服务
docker-compose up -d scheduler

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 优点
- ✅ 环境隔离
- ✅ 易于部署
- ✅ 可移植性强

## ☁️ 方式三：云服务器部署

适合需要高频抓取的用户。

### AWS EC2

1. **启动 EC2 实例**
   - 选择 Amazon Linux 2 或 Ubuntu
   - 配置安全组，允许 SSH (22)

2. **连接实例**
   ```bash
   ssh -i your-key.pem ec2-user@your-ip
   ```

3. **安装依赖**
   ```bash
   sudo yum update -y
   sudo yum install python3 -y
   pip3 install -r requirements.txt
   ```

4. **设置定时任务**
   ```bash
   crontab -e
   # 添加：每天早上9点运行
   0 9 * * 1-5 cd /home/ec2-user/stock-bot && python3 src/main.py
   ```

### 阿里云 ECS

1. **购买 ECS 实例**
   - 选择 CentOS 或 Ubuntu
   - 配置安全组

2. **部署步骤**
   ```bash
   # 安装 Python
   yum install python3 -y
   
   # 克隆代码
   git clone https://github.com/yourusername/stock-bot.git
   cd stock-bot
   
   # 安装依赖
   pip3 install -r requirements.txt
   
   # 设置定时任务
   crontab -e
   ```

### 优点
- ✅ 完全控制
- ✅ 高频运行
- ✅ 稳定可靠

## 🖥️ 方式四：本地服务器部署

适合个人使用。

### Windows

1. **安装 Python**
   - 下载 Python 3.9+
   - 安装时勾选 "Add Python to PATH"

2. **设置定时任务**
   ```powershell
   # 打开任务计划程序
   taskschd.msc
   
   # 创建基本任务
   # 设置触发器：每天
   # 设置操作：启动程序
   # 程序：python
   # 参数：C:\path\to\stock-bot\src\main.py
   ```

### Linux/Mac

1. **安装 Python**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip
   
   # Mac
   brew install python3
   ```

2. **设置定时任务**
   ```bash
   # 编辑 crontab
   crontab -e
   
   # 添加：每天早上9点运行
   0 9 * * 1-5 cd /path/to/stock-bot && python3 src/main.py
   ```

## 📊 数据存储方案

### 本地存储

数据保存在 `data/` 目录：
```
data/
├── stock_data_20240115_090000.json
├── global_AAPL_20240115_090000.csv
└── a_share_realtime_20240115_090000.csv
```

### 云存储（可选）

修改 `src/main.py` 添加云存储支持：

```python
# 保存到 AWS S3
import boto3

def upload_to_s3(file_path, bucket_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, file_path)
```

### 数据库存储（可选）

修改 `src/main.py` 添加数据库支持：

```python
# 保存到 SQLite
import sqlite3

def save_to_db(data, db_path):
    conn = sqlite3.connect(db_path)
    # 创建表并插入数据
    conn.close()
```

## 🔧 监控和日志

### 日志配置

修改 `src/main.py` 添加日志：

```python
import logging

logging.basicConfig(
    filename='stock-bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### 监控脚本

创建 `monitor.py`：

```python
import os
from datetime import datetime

def check_data_freshness():
    data_dir = 'data'
    files = os.listdir(data_dir)
    if not files:
        print("警告: 没有数据文件")
        return
    
    latest_file = max(files)
    print(f"最新数据文件: {latest_file}")
```

## 🚨 常见问题

### Q: 网络连接失败

A: 检查网络连接，可能需要配置代理：
```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
```

### Q: API 限制

A: 添加请求间隔：
```python
import time
time.sleep(1)  # 每次请求间隔1秒
```

### Q: 内存不足

A: 分批处理数据：
```python
# 分批处理
batch_size = 100
for i in range(0, len(symbols), batch_size):
    batch = symbols[i:i+batch_size]
    # 处理批次
```

### Q: 磁盘空间不足

A: 定期清理旧数据：
```python
import os
from datetime import datetime, timedelta

def cleanup_old_data(data_dir, days=30):
    cutoff = datetime.now() - timedelta(days=days)
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        if os.path.getmtime(file_path) < cutoff.timestamp():
            os.remove(file_path)
```

## 📞 获取帮助

如果遇到问题：

1. 查看 [README.md](README.md) 了解基本使用
2. 查看 [QUICKSTART.md](QUICKSTART.md) 了解快速开始
3. 查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献
4. 提交 GitHub Issue