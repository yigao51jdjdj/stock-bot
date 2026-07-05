@echo off
echo 股票数据抓取机器人 - 快速启动
echo ================================

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 安装依赖
echo.
echo 1. 安装依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 依赖安装失败
    pause
    exit /b 1
)

REM 运行测试
echo.
echo 2. 运行测试...
python test_scraper.py
if errorlevel 1 (
    echo 测试失败
    pause
    exit /b 1
)

echo.
echo 3. 运行数据抓取...
python src/main.py

echo.
echo 完成！
pause