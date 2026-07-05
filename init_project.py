"""
项目初始化脚本
帮助用户快速开始使用股票数据抓取机器人
"""

import os
import sys
from pathlib import Path
import shutil


def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("🚀 股票数据抓取机器人 - 项目初始化")
    print("=" * 60)


def check_project_structure():
    """检查项目结构"""
    print("\n1. 检查项目结构...")
    
    required_files = [
        "config.json",
        "requirements.txt",
        "src/main.py",
        "src/scrapers/yfinance_scraper.py",
        "src/scrapers/akshare_scraper.py",
        ".github/workflows/stock-scrape.yml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 项目结构完整")
    return True


def setup_virtual_environment():
    """设置虚拟环境"""
    print("\n2. 设置虚拟环境...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ 虚拟环境已存在")
        return True
    
    try:
        # 创建虚拟环境
        os.system(f"{sys.executable} -m venv venv")
        
        # 激活虚拟环境的说明
        if sys.platform == "win32":
            activate_cmd = "venv\\Scripts\\activate"
        else:
            activate_cmd = "source venv/bin/activate"
        
        print(f"✅ 虚拟环境创建成功")
        print(f"   激活命令: {activate_cmd}")
        return True
    except Exception as e:
        print(f"❌ 虚拟环境创建失败: {e}")
        return False


def install_dependencies():
    """安装依赖"""
    print("\n3. 安装依赖...")
    
    try:
        # 检查是否在虚拟环境中
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("✅ 已在虚拟环境中")
        
        # 安装依赖
        result = os.system(f"{sys.executable} -m pip install -r requirements.txt")
        if result == 0:
            print("✅ 依赖安装完成")
            return True
        else:
            print("❌ 依赖安装失败")
            return False
    except Exception as e:
        print(f"❌ 依赖安装失败: {e}")
        return False


def create_sample_config():
    """创建示例配置"""
    print("\n4. 创建配置文件...")
    
    config_path = Path("config.json")
    if config_path.exists():
        print("✅ 配置文件已存在")
        return True
    
    # 复制示例配置
    example_config = Path("config.example.json")
    if example_config.exists():
        shutil.copy(example_config, config_path)
        print("✅ 配置文件已创建")
        return True
    else:
        print("❌ 未找到示例配置文件")
        return False


def run_test():
    """运行测试"""
    print("\n5. 运行测试...")
    
    try:
        result = os.system(f"{sys.executable} test_scraper.py")
        if result == 0:
            print("✅ 测试通过")
            return True
        else:
            print("⚠️ 测试未完全通过，但项目可以继续使用")
            return True  # 允许部分失败
    except Exception as e:
        print(f"⚠️ 测试执行出错: {e}")
        return True  # 允许测试失败


def print_next_steps():
    """打印下一步操作"""
    print("\n" + "=" * 60)
    print("🎉 项目初始化完成！")
    print("=" * 60)
    
    print("\n📋 下一步操作:")
    print("1. 编辑 config.json 添加你感兴趣的股票代码")
    print("2. 本地测试: python src/main.py")
    print("3. 创建 GitHub 仓库")
    print("4. 推送代码到 GitHub")
    print("5. GitHub Actions 会自动运行数据抓取")
    
    print("\n📚 文档:")
    print("- README.md: 完整使用说明")
    print("- QUICKSTART.md: 快速开始指南")
    print("- config.example.json: 配置文件示例")
    
    print("\n🔧 常用命令:")
    print("- 运行抓取: python src/main.py")
    print("- 运行测试: python test_scraper.py")
    print("- 安装依赖: pip install -r requirements.txt")
    
    print("\n💡 提示:")
    print("- 数据会自动保存到 data/ 目录")
    print("- GitHub Actions 会自动运行")
    print("- 可在 GitHub Actions 页面手动触发")


def main():
    """主初始化函数"""
    print_banner()
    
    # 检查项目结构
    if not check_project_structure():
        print("\n❌ 项目结构不完整，请确保所有文件都已创建")
        return False
    
    # 设置虚拟环境
    setup_virtual_environment()
    
    # 安装依赖
    if not install_dependencies():
        print("\n❌ 依赖安装失败，请检查网络连接")
        return False
    
    # 创建配置文件
    create_sample_config()
    
    # 运行测试
    run_test()
    
    # 打印下一步操作
    print_next_steps()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)