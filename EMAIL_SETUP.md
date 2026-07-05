# iCloud 邮箱配置完成

## ✅ 配置信息

| 配置项 | 值 |
|--------|-----|
| SMTP 服务器 | smtp.mail.me.com |
| 端口 | 465 (SSL) |
| 发送邮箱 | gao_hong1@icloud.com |
| 接收邮箱 | gao_hong1@icloud.com |

## 📧 邮件内容示例

每次推送将包含以下信息：

```
📈 每日股票行情汇总
==============================

【科技股】
AAPL Apple Inc.      308.63 USD (+1.20%)
GOOGL Alphabet Inc.  359.91 USD (-0.80%)
MSFT Microsoft       390.49 USD (+0.75%)
...

【半导体】
NVDA NVIDIA Corp.    194.83 USD (+2.30%)
...

⏰ 2024-01-15 22:00:00
```

## 🚀 部署到 GitHub

### 1. 推送代码

```bash
cd stock-bot
git init
git add .
git commit -m "Initial commit: Stock bot with email notifications"
git remote add origin https://github.com/你的用户名/stock-bot.git
git push -u origin main
```

### 2. 配置 GitHub Secrets

进入仓库 **Settings → Secrets and variables → Actions**，添加以下 Secrets：

| Secret 名称 | 值 |
|-------------|-----|
| `EMAIL_SENDER` | gao_hong1@icloud.com |
| `EMAIL_PASSWORD` | cudt-imxa-cwct-tfze |
| `EMAIL_RECEIVER` | gao_hong1@icloud.com |

### 3. 启用 GitHub Actions

1. 进入仓库 **Actions** 标签
2. 点击 **"I understand my workflows, go ahead and enable them"**

### 4. 手动测试

1. 点击 **Actions** → **Stock Data Scraper**
2. 点击 **Run workflow**
3. 选择通知类型：`summary`
4. 等待运行完成，检查邮箱

## ⏰ 推送时间

| 时间 (北京时间) | 说明 |
|----------------|------|
| 09:00 | 早盘开盘 |
| 13:00 | 午盘开盘 |
| 22:00 | 美股开盘 |

## 🔧 本地测试

```bash
# 测试邮件发送
python src/main.py --notify-type summary

# 仅抓取不发送通知
python src/main.py --no-notify
```

## ❓ 常见问题

### Q: 邮件没有收到？

A: 检查以下几点：
1. iCloud 应用专用密码是否正确
2. 垃圾邮件文件夹
3. GitHub Actions 运行日志

### Q: 如何修改推送时间？

A: 编辑 `.github/workflows/stock-scrape.yml` 中的 `schedule` 部分。

### Q: 可以发送到其他邮箱吗？

A: 可以，修改 `config.json` 中的 `receiver` 字段即可。

### Q: 如何添加更多股票？

A: 编辑 `config.json` 中的 `global_symbols` 和 `a_share_symbols` 数组。