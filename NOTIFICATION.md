# 通知推送配置指南

本项目支持多种通知渠道，可以将股票行情推送到你的手机或邮箱。

## 支持的通知渠道

| 渠道 | 说明 | 配置难度 |
|------|------|----------|
| Telegram | Telegram 机器人 | 简单 |
| 钉钉 | 钉钉群机器人 | 简单 |
| 企业微信 | 企业微信群机器人 | 简单 |
| 邮件 | 邮件通知 | 中等 |

## 快速配置

### 1. Telegram 机器人

#### 创建 Bot
1. 在 Telegram 搜索 `@BotFather`
2. 发送 `/newbot` 创建新机器人
3. 获取 Bot Token

#### 获取 Chat ID
1. 将机器人添加到群组或直接私聊
2. 访问 `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. 找到 `chat.id` 字段

#### 配置方式

**方式一：编辑 config.json**
```json
{
  "notifications": {
    "telegram": {
      "enabled": true,
      "bot_token": "YOUR_BOT_TOKEN",
      "chat_id": "YOUR_CHAT_ID"
    }
  }
}
```

**方式二：GitHub Secrets（推荐）**
1. 进入仓库 Settings -> Secrets and variables -> Actions
2. 添加以下 Secrets:
   - `TELEGRAM_BOT_TOKEN`: Bot Token
   - `TELEGRAM_CHAT_ID`: Chat ID

---

### 2. 钉钉机器人

#### 创建机器人
1. 打开钉钉群 -> 群设置 -> 智能群助手
2. 添加自定义机器人
3. 获取 Webhook URL

#### 配置方式

**config.json:**
```json
{
  "notifications": {
    "dingtalk": {
      "enabled": true,
      "webhook_url": "https://oapi.dingtalk.com/robot/send?access_token=xxx"
    }
  }
}
```

**GitHub Secrets:**
- `DINGTALK_WEBHOOK_URL`: Webhook URL

---

### 3. 企业微信机器人

#### 创建机器人
1. 打开企业微信群 -> 群设置 -> 群机器人
2. 添加机器人
3. 获取 Webhook URL

#### 配置方式

**config.json:**
```json
{
  "notifications": {
    "wechat": {
      "enabled": true,
      "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
    }
  }
}
```

**GitHub Secrets:**
- `WECHAT_WEBHOOK_URL`: Webhook URL

---

### 4. 邮件通知

#### 获取邮箱授权码

**Gmail:**
1. 开启两步验证
2. 生成应用专用密码
3. 使用应用专用密码

**QQ 邮箱:**
1. 设置 -> 账户 -> 开启 SMTP 服务
2. 生成授权码

**163 邮箱:**
1. 设置 -> POP3/SMTP/IMAP
2. 开启 SMTP 服务
3. 生成授权码

#### 配置方式

**config.json:**
```json
{
  "notifications": {
    "email": {
      "enabled": true,
      "smtp_host": "smtp.gmail.com",
      "smtp_port": 465,
      "sender": "your_email@gmail.com",
      "password": "your_app_password",
      "receiver": "receiver@example.com"
    }
  }
}
```

**GitHub Secrets:**
- `EMAIL_SENDER`: 发送邮箱
- `EMAIL_PASSWORD`: 邮箱密码/授权码
- `EMAIL_RECEIVER`: 接收邮箱

---

## 常用邮箱 SMTP 配置

| 邮箱 | SMTP 服务器 | 端口 |
|------|-------------|------|
| Gmail | smtp.gmail.com | 465 |
| QQ 邮箱 | smtp.qq.com | 465 |
| 163 邮箱 | smtp.163.com | 465 |
| Outlook | smtp.office365.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 465 |

---

## 定时推送时间

项目默认配置为每日三次推送：

| 时间 (北京时间) | Cron 表达式 | 说明 |
|----------------|-------------|------|
| 09:00 | `0 1 * * 1-5` | 早盘开盘 |
| 13:00 | `0 5 * * 1-5` | 午盘开盘 |
| 22:00 | `0 14 * * 1-5` | 美股开盘 |

如需修改，编辑 `.github/workflows/stock-scrape.yml` 中的 `schedule` 部分。

---

## 手动触发

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "Stock Data Scraper"
4. 点击 "Run workflow"
5. 选择通知类型：
   - `price`: 实时价格提醒
   - `summary`: 每日汇总

---

## 消息示例

### 价格提醒 (price)
```
📊 股票行情提醒
==============================
AAPL Apple Inc.       308.63 USD (+1.25%)
GOOGL Alphabet Inc.   359.91 USD (-0.50%)
...

⏰ 2024-01-15 09:00:00
```

### 每日汇总 (summary)
```
📈 每日股票行情汇总
==============================

【科技股】
AAPL Apple Inc.       308.63 USD (+1.25%)
GOOGL Alphabet Inc.   359.91 USD (-0.50%)
...

【半导体】
NVDA NVIDIA Corp.     194.83 USD (+2.30%)
...

⏰ 2024-01-15 22:00:00
```

---

## 常见问题

### Q: 通知没有收到？

A: 检查以下几点：
1. 配置是否正确
2. GitHub Actions 是否运行成功
3. 是否在 GitHub Secrets 中配置了密钥
4. 邮箱是否开启了 SMTP 服务

### Q: 如何测试通知？

A: 在 GitHub Actions 页面手动触发 workflow，选择通知类型。

### Q: 可以同时使用多个渠道吗？

A: 可以，只需在 config.json 中同时启用多个渠道即可。

### Q: 推送时间可以修改吗？

A: 可以，编辑 `.github/workflows/stock-scrape.yml` 中的 cron 表达式。