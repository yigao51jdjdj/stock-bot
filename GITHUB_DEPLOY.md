# GitHub 部署指南

## 📋 部署步骤

### 步骤 1: 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 仓库名称填写: `stock-bot`
3. 选择 **Public** 或 **Private**
4. **不要**勾选 "Add a README file"（我们已有本地代码）
5. 点击 **Create repository**

### 步骤 2: 推送代码

创建仓库后，运行以下命令：

```bash
cd C:\Users\Administrator\stock-bot
git push -u origin master
```

### 步骤 3: 配置 GitHub Secrets

推送成功后，进入仓库设置：

1. 访问 https://github.com/in-stock/stock-bot/settings/secrets/actions
2. 点击 **New repository secret**
3. 添加以下 Secrets:

| Name | Value |
|------|-------|
| `EMAIL_SENDER` | gao_hong1@icloud.com |
| `EMAIL_PASSWORD` | cudt-imxa-cwct-tfze |
| `EMAIL_RECEIVER` | gao_hong1@icloud.com |

### 步骤 4: 启用 GitHub Actions

1. 访问 https://github.com/in-stock/stock-bot/actions
2. 点击 **"I understand my workflows, go ahead and enable them"**

### 步骤 5: 手动测试

1. 点击 **Stock Data Scraper**
2. 点击 **Run workflow**
3. 等待运行完成
4. 检查邮箱是否收到通知

## ⏰ 自动运行时间

配置完成后，系统将每日自动运行三次：

| 时间 (北京时间) | 说明 |
|----------------|------|
| 09:00 | 早盘开盘 |
| 13:00 | 午盘开盘 |
| 22:00 | 美股开盘 |

## ❓ 常见问题

### Q: 推送失败？

A: 检查是否已登录 GitHub。可以在终端运行：
```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

### Q: 如何查看运行日志？

A: 访问 https://github.com/in-stock/stock-bot/actions 查看。

### Q: 如何修改推送时间？

A: 编辑 `.github/workflows/stock-scrape.yml` 中的 cron 表达式。