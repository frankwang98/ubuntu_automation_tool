#!/usr/bin/env python3
"""Windows Automation Tool"""
import os
import subprocess
import platform
import sys
from datetime import datetime
from typing import Dict, Optional

VERSION = "1.0.0 - " + datetime.now().strftime("%Y-%m-%d")


class WindowsAutomationTool:
    def __init__(self):
        self.main_menu = {
            "1": {"name": "系统信息查询", "func": self.system_info},
            "2": {"name": "系统更新", "func": self.system_update},
            "3": {"name": "系统清理", "func": self.system_clean},
            "4": {"name": "安装软件", "func": self.install_software},
            "5": {"name": "Docker管理", "func": self.docker_management},
            "6": {"name": "网络工具", "func": self.network_tools},
            "7": {"name": "小游戏专区", "func": self.game_zone},
            "10": {"name": "退出", "func": self.exit_tool}
        }

    def run_command(self, command: str, powershell: bool = True) -> None:
        """执行命令"""
        try:
            if powershell:
                subprocess.run(["powershell.exe", "-Command", command], check=True)
            else:
                subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")

    def run_command_output(self, command: str, powershell: bool = True) -> str:
        """执行命令并返回输出"""
        try:
            if powershell:
                result = subprocess.run(
                    ["powershell.exe", "-Command", command],
                    capture_output=True, text=True, check=True
                )
                return result.stdout
            else:
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True, check=True
                )
                return result.stdout
        except subprocess.CalledProcessError as e:
            return f"命令执行失败: {e}"

    def display_menu(self, menu: Dict, title: str) -> None:
        """显示菜单"""
        print(f"\n=== {title} ===")
        for key, value in menu.items():
            print(f"{key}. {value['name']}")

    def get_user_choice(self, menu: Dict) -> Optional[str]:
        """获取用户选择"""
        while True:
            choice = input("\n请输入数字选择 (q退出): ").strip()
            if choice.lower() == 'q':
                return None
            if choice in menu:
                return choice
            print("无效输入，请重新选择")

    def system_info(self) -> None:
        """系统信息查询"""
        print("\n=== 系统信息 ===")
        print(f"计算机名: {platform.node()}")
        print(f"操作系统: {platform.platform()}")
        print(f"版本: {platform.version()}")
        print(f"架构: {platform.machine()}")
        print(f"处理器: {platform.processor()}")

    def system_update(self) -> None:
        """系统更新"""
        print("\n正在检查 Windows 更新...")
        self.run_command("Start-Process ms-settings:windowsupdate")

    def system_clean(self) -> None:
        """系统清理"""
        print("\n=== 系统清理 ===")
        print("1. 清理临时文件")
        print("2. 清理回收站")
        print("3. 磁盘清理")
        print("4. 返回主菜单")

        choice = input("\n请选择: ").strip()
        if choice == "1":
            print("清理临时文件...")
            self.run_command("Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue")
            print("完成")
        elif choice == "2":
            print("清理回收站...")
            self.run_command("Clear-RecycleBin -Force -ErrorAction SilentlyContinue")
            print("完成")
        elif choice == "3":
            print("打开磁盘清理...")
            self.run_command("cleanmgr")

    def install_software(self) -> None:
        """安装软件"""
        print("\n=== 安装软件 ===")
        print("1. 安装 Visual Studio Code")
        print("2. 安装 Git")
        print("3. 安装 Python")
        print("4. 安装 Docker Desktop")
        print("5. 安装 Node.js")
        print("6. 返回主菜单")

        choice = input("\n请选择: ").strip()
        commands = {
            "1": 'winget install Microsoft.VisualStudioCode',
            "2": 'winget install Git.Git',
            "3": 'winget install Python.Python.3.11',
            "4": 'winget install Docker.DockerDesktop',
            "5": 'winget install OpenJS.NodeJS.LTS'
        }

        if choice in commands:
            print(f"正在安装...")
            self.run_command(commands[choice])
            print("安装完成")

    def docker_management(self) -> None:
        """Docker管理"""
        print("\n=== Docker 管理 ===")
        print("1. 查看 Docker 状态")
        print("2. 启动 Docker")
        print("3. 停止 Docker")
        print("4. 返回主菜单")

        choice = input("\n请选择: ").strip()
        if choice == "1":
            output = self.run_command_output("docker version")
            print(output or "Docker 未安装或未运行")
        elif choice == "2":
            print("启动 Docker...")
            self.run_command("Start-Service Docker")
        elif choice == "3":
            print("停止 Docker...")
            self.run_command("Stop-Service Docker")

    def network_tools(self) -> None:
        """网络工具"""
        print("\n=== 网络工具 ===")
        print("1. 查看 IP 地址")
        print("2. 测试网络连接")
        print("3. 查看网络配置")
        print("4. 返回主菜单")

        choice = input("\n请选择: ").strip()
        if choice == "1":
            output = self.run_command_output("ipconfig | Select-String 'IPv4'")
            print(output)
        elif choice == "2":
            target = input("请输入测试地址: ").strip() or "8.8.8.8"
            output = self.run_command_output(f"Test-NetConnection {target}")
            print(output)
        elif choice == "3":
            output = self.run_command_output("Get-NetIPConfiguration")
            print(output)

    def game_zone(self) -> None:
        """小游戏专区"""
        print("\n=== 小游戏专区 ===")
        print("1. 数字猜谜")
        print("2. 返���主菜单")

        choice = input("\n请选择: ").strip()
        if choice == "1":
            self.number_guessing_game()

    def number_guessing_game(self) -> None:
        """数字猜谜游戏"""
        print("\n=== 数字猜谜游戏 ===")
        print("我将生成一个 1-100 的随机数字，请猜猜看！")

        import random
        target = random.randint(1, 100)
        attempts = 0

        while True:
            try:
                guess = int(input("\n请输入数字: ").strip())
            except ValueError:
                print("请输入有效数字")
                continue

            attempts += 1

            if guess < target:
                print("太小了！")
            elif guess > target:
                print("太大了！")
            else:
                print(f"恭喜！用了 {attempts} 次猜对了！")
                break

    def exit_tool(self) -> None:
        """退出工具"""
        print("\n感谢使用！再见！")
        sys.exit(0)

    def run(self) -> None:
        """运行主循环"""
        while True:
            self.display_menu(self.main_menu, "Windows 自动化工具")
            choice = self.get_user_choice(self.main_menu)

            if choice is None or choice == "10":
                self.exit_tool()

            if choice in self.main_menu:
                func = self.main_menu[choice].get("func")
                if func:
                    func()


def main():
    tool = WindowsAutomationTool()
    tool.run()


if __name__ == "__main__":
    main()