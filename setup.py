"""
股票数据抓取机器人 - 快速设置脚本
"""

import os
import sys
from pathlib import Path
import subprocess


def check_python_version():
    """检查 Python 版本"""
    if sys.version_info < (3, 8):
        print("错误: 需要 Python 3.8 或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"Python 版本: {sys.version}")
    return True


def install_requirements():
    """安装依赖"""
    print("\n安装依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖安装完成!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False


def create_directories():
    """创建必要的目录"""
    print("\n创建目录结构...")
    dirs = ["data", "src/scrapers", ".github/workflows"]
    for dir_name in dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        print(f"  创建目录: {dir_name}")
    return True


def create_sample_config():
    """创建示例配置文件"""
    print("\n创建配置文件...")
    config_content = '''{
  "global_symbols": ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"],
  "a_share_symbols": ["600519", "000858", "300750"],
  "data_dir": "data",
  "output_format": "json",
  "fetch_historical_days": 30
}'''
    
    config_path = Path("config.json")
    if not config_path.exists():
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)
        print("  创建配置文件: config.json")
    else:
        print("  配置文件已存在")
    return True


def main():
    """主设置函数"""
    print("=" * 60)
    print("股票数据抓取机器人 - 快速设置")
    print("=" * 60)
    
    # 检查 Python 版本
    if not check_python_version():
        return False
    
    # 创建目录
    if not create_directories():
        return False
    
    # 安装依赖
    if not install_requirements():
        return False
    
    # 创建配置文件
    if not create_sample_config():
        return False
    
    print("\n" + "=" * 60)
    print("设置完成!")
    print("=" * 60)
    print("\n下一步:")
    print("1. 编辑 config.json 文件，添加你感兴趣的股票代码")
    print("2. 运行测试: python test_scraper.py")
    print("3. 本地测试: python src/main.py")
    print("4. 创建 GitHub 仓库并推送代码")
    print("\nGitHub Actions 会自动按计划运行数据抓取任务!")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)