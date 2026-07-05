# 贡献指南

感谢你对股票数据抓取机器人的贡献！本指南将帮助你开始贡献代码。

## 🎯 如何贡献

### 1. 报告问题

如果你发现了一个问题，请：

1. 检查 [Issues](https://github.com/yourusername/stock-bot/issues) 是否已有相同问题
2. 如果没有，创建一个新的 Issue
3. 提供详细的问题描述和复现步骤

### 2. 提交代码

#### 步骤 1: Fork 仓库

```bash
# 在 GitHub 上 Fork 仓库
git clone https://github.com/yourusername/stock-bot.git
cd stock-bot
git remote add upstream https://github.com/originalusername/stock-bot.git
```

#### 步骤 2: 创建分支

```bash
# 从 main 分支创建新分支
git checkout -b feature/your-feature-name

# 或修复 bug
git checkout -b fix/your-bug-fix
```

#### 步骤 3: 进行修改

- 遵循现有的代码风格
- 添加必要的注释
- 确保代码可以正常运行

#### 步骤 4: 测试你的修改

```bash
# 运行测试
python test_scraper.py

# 本地测试
python src/main.py
```

#### 步骤 5: 提交代码

```bash
# 添加修改
git add .

# 提交修改
git commit -m "feat: 添加新功能描述"

# 推送到你的 Fork
git push origin feature/your-feature-name
```

#### 步骤 6: 创建 Pull Request

1. 在 GitHub 上打开你的 Fork
2. 点击 "Compare & pull request"
3. 填写 PR 描述
4. 提交 PR

## 📝 代码规范

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

#### 示例

```bash
# 新功能
git commit -m "feat(scraper): 添加新的数据源支持"

# Bug 修复
git commit -m "fix(yfinance): 修复网络超时问题"

# 文档更新
git commit -m "docs: 更新 README 中的使用说明"
```

### 代码风格

- 使用 4 个空格缩进
- 遵循 PEP 8 规范
- 使用类型提示
- 添加必要的文档字符串

### 文件组织

```
src/
├── scrapers/           # 数据抓取器
│   ├── __init__.py
│   ├── yfinance_scraper.py
│   └── akshare_scraper.py
├── utils/              # 工具函数
│   ├── __init__.py
│   └── helpers.py
└── main.py             # 主入口
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
python test_scraper.py

# 运行特定测试
python -m pytest tests/
```

### 添加测试

如果你添加了新功能，请添加相应的测试：

```python
# tests/test_new_feature.py
import unittest
from src.scrapers.new_scraper import NewScraper

class TestNewScraper(unittest.TestCase):
    def test_fetch_data(self):
        scraper = NewScraper()
        data = scraper.fetch_data()
        self.assertIsNotNone(data)

if __name__ == "__main__":
    unittest.main()
```

## 📚 文档

### 更新文档

如果你添加了新功能，请更新相关文档：

1. **README.md**: 更新功能列表和使用说明
2. **QUICKSTART.md**: 更新快速开始指南
3. **代码注释**: 添加必要的文档字符串

### 文档风格

- 使用 Markdown 格式
- 提供清晰的示例
- 包含必要的说明

## 🐛 报告 Bug

报告 Bug 时请包含：

1. **问题描述**: 清晰描述遇到的问题
2. **复现步骤**: 详细的操作步骤
3. **期望行为**: 期望的正确行为
4. **实际行为**: 实际发生的情况
5. **环境信息**: 
   - 操作系统
   - Python 版本
   - 相关依赖版本

### Bug 报告模板

```markdown
## Bug 描述

简要描述遇到的问题

## 复现步骤

1. 执行 `python src/main.py`
2. 配置 config.json
3. 运行抓取
4. 出现错误

## 期望行为

期望的正确行为

## 实际行为

实际发生的情况

## 环境信息

- 操作系统: Windows 10
- Python 版本: 3.9.7
- 依赖版本: yfinance 0.2.36

## 日志信息

如果有错误日志，请粘贴在这里
```

## ✨ 新功能建议

建议新功能时请包含：

1. **功能描述**: 清晰描述期望的功能
2. **使用场景**: 说明这个功能的使用场景
3. **实现建议**: 如果有想法，可以提供实现建议

## 📞 联系方式

如果你有任何问题，可以通过以下方式联系：

- GitHub Issues: [项目 Issues 页面]
- Email: your.email@example.com

## 📜 许可证

贡献的代码将采用 MIT 许可证。

感谢你的贡献！🎉