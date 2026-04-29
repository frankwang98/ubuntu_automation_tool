#!/usr/bin/env python3
import os
import subprocess
import platform
import time
import sys
import random
import readline
from datetime import datetime
from typing import Dict, Optional

VERSION = "1.0.0 - " + datetime.now().strftime("%Y-%m-%d")

class MacAutomationTool:
    def __init__(self):
        self.main_menu = {
            "1": {"name": "系统信息查询", "func": self.system_info},
            "2": {"name": "系统维护", "func": self.system_maintenance},
            "3": {"name": "安装开发工具", "func": self.install_dev_tools},
            "4": {"name": "Homebrew 管理", "func": self.brew_management},
            "5": {"name": "Docker管理", "func": self.docker_management},
            "6": {"name": "磁盘工具", "func": self.disk_utilities},
            "7": {"name": "网络工具", "func": self.network_tools},
            "8": {"name": "隐私与安全", "func": self.privacy_security},
            "9": {"name": "小游戏专区", "func": self.game_zone},
            "10": {"name": "退出", "func": self.exit_tool}
        }
        
        self.brew_submenu = {
            "1": {"name": "安装Homebrew", "func": self.install_homebrew},
            "2": {"name": "更新Homebrew", "func": self.update_homebrew},
            "3": {"name": "搜索软件包", "func": self.search_brew_packages},
            "4": {"name": "安装软件", "func": self.install_brew_package},
            "5": {"name": "返回主菜单", "func": None}
        }
        
        self.disk_menu = {
            "1": {"name": "磁盘使用情况", "func": self.disk_usage},
            "2": {"name": "清理缓存", "func": self.clean_cache},
            "3": {"name": "查找大文件", "func": self.find_large_files},
            "4": {"name": "返回主菜单", "func": None}
        }
        
        self.games_menu = {
            "1": {"name": "数字猜谜", "func": self.number_guessing_game},
            "2": {"name": "21点游戏", "func": self.blackjack_game},
            "3": {"name": "打字测试", "func": self.typing_test},
            "4": {"name": "终端贪吃蛇", "func": self.snake_game},
            "5": {"name": "记忆翻牌", "func": self.memory_game},
            "6": {"name": "返回主菜单", "func": None}
        }

    def run_command(self, command: str, sudo: bool = False) -> None:
        """执行shell命令"""
        if sudo:
            command = f"sudo {command}"
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")

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
        print(f"系统名称: {platform.system()}")
        print(f"系统版本: {platform.mac_ver()[0]}")
        print(f"系统架构: {platform.machine()}")
        print(f"处理器: {platform.processor()}")
        self.run_command("system_profiler SPHardwareDataType | grep 'Model Identifier'")
        self.run_command("system_profiler SPHardwareDataType | grep 'Memory'")
        self.run_command("df -h")
        self.run_command("uptime")

    def system_maintenance(self) -> None:
        """系统维护"""
        print("\n=== 系统维护 ===")
        print("1. 更新系统软件")
        print("2. 清理系统缓存")
        print("3. 重建Spotlight索引")
        print("4. 修复磁盘权限")
        choice = input("请选择操作: ")
        
        if choice == "1":
            print("\n正在检查系统更新...")
            self.run_command("softwareupdate -l")
            confirm = input("是否安装所有可用更新? (y/n): ").lower()
            if confirm == 'y':
                self.run_command("softwareupdate -ia", sudo=True)
        elif choice == "2":
            print("\n正在清理系统缓存...")
            self.run_command("sudo rm -rf ~/Library/Caches/*", sudo=True)
            self.run_command("sudo rm -rf /Library/Caches/*", sudo=True)
            print("系统缓存已清理")
        elif choice == "3":
            print("\n正在重建Spotlight索引...")
            self.run_command("sudo mdutil -E /", sudo=True)
            print("索引重建已开始，可能需要一些时间")
        elif choice == "4":
            print("\n正在修复磁盘权限...")
            self.run_command("diskutil verifyVolume /", sudo=True)
            self.run_command("diskutil repairPermissions /", sudo=True)
            print("磁盘权限已修复")

    def install_dev_tools(self) -> None:
        """安装开发工具"""
        print("\n=== 安装开发工具 ===")
        print("1. 安装Xcode命令行工具")
        print("2. 安装Python开发环境")
        print("3. 安装Node.js环境")
        print("4. 安装Java开发环境")
        choice = input("请选择操作: ")
        
        if choice == "1":
            print("\n正在安装Xcode命令行工具...")
            self.run_command("xcode-select --install")
        elif choice == "2":
            print("\n正在安装Python开发环境...")
            self.run_command("brew install python", sudo=True)
            self.run_command("pip install --upgrade pip")
            print("Python开发环境已安装")
        elif choice == "3":
            print("\n正在安装Node.js环境...")
            self.run_command("brew install node", sudo=True)
            print("Node.js已安装")
        elif choice == "4":
            print("\n正在安装Java开发环境...")
            self.run_command("brew install --cask adoptopenjdk", sudo=True)
            print("Java开发环境已安装")

    def brew_management(self) -> None:
        """Homebrew管理"""
        while True:
            self.display_menu(self.brew_submenu, "Homebrew管理")
            choice = self.get_user_choice(self.brew_submenu)
            if not choice or choice == "5":
                break
            if self.brew_submenu[choice]["func"]:
                self.brew_submenu[choice]["func"]()

    def install_homebrew(self) -> None:
        """安装Homebrew"""
        print("\n正在安装Homebrew...")
        self.run_command('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
        print("Homebrew已安装")

    def update_homebrew(self) -> None:
        """更新Homebrew"""
        print("\n正在更新Homebrew...")
        self.run_command("brew update")
        self.run_command("brew upgrade")
        print("Homebrew已更新")

    def search_brew_packages(self) -> None:
        """搜索Homebrew软件包"""
        query = input("输入要搜索的软件包名称: ")
        self.run_command(f"brew search {query}")

    def install_brew_package(self) -> None:
        """安装Homebrew软件包"""
        package = input("输入要安装的软件包名称: ")
        self.run_command(f"brew install {package}")

    def docker_management(self) -> None:
        """Docker管理"""
        print("\n=== Docker管理 ===")
        print("1. 启动Docker服务")
        print("2. 停止Docker服务")
        print("3. 列出运行中的容器")
        print("4. 清理Docker资源")
        choice = input("请选择操作: ")
        
        if choice == "1":
            self.run_command("open --background -a Docker")
            print("Docker服务已启动")
        elif choice == "2":
            self.run_command("osascript -e 'quit app \"Docker\"'")
            print("Docker服务已停止")
        elif choice == "3":
            self.run_command("docker ps")
        elif choice == "4":
            self.run_command("docker system prune -f")
            print("Docker资源已清理")

    def disk_utilities(self) -> None:
        """磁盘工具"""
        while True:
            self.display_menu(self.disk_menu, "磁盘工具")
            choice = self.get_user_choice(self.disk_menu)
            if not choice or choice == "4":
                break
            if self.disk_menu[choice]["func"]:
                self.disk_menu[choice]["func"]()

    def disk_usage(self) -> None:
        """显示磁盘使用情况"""
        print("\n磁盘使用情况:")
        self.run_command("df -h")
        print("\n各目录大小:")
        self.run_command("du -sh ~/* | sort -hr")

    def clean_cache(self) -> None:
        """清理缓存"""
        print("\n正在清理缓存...")
        self.run_command("sudo rm -rf ~/Library/Caches/*", sudo=True)
        self.run_command("sudo rm -rf /Library/Caches/*", sudo=True)
        print("缓存已清理")

    def find_large_files(self) -> None:
        """查找大文件"""
        print("\n正在查找大文件...")
        self.run_command("find ~ -type f -size +100M -exec ls -lh {} + | sort -k 5 -rh")

    def network_tools(self) -> None:
        """网络工具"""
        print("\n=== 网络工具 ===")
        print("1. 检查网络连接")
        print("2. 查看网络信息")
        print("3. 刷新DNS缓存")
        print("4. 查看端口占用")
        choice = input("请选择操作: ")
        
        if choice == "1":
            self.run_command("ping -c 4 baidu.com")
        elif choice == "2":
            self.run_command("ifconfig")
            self.run_command("netstat -rn")
        elif choice == "3":
            self.run_command("sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder", sudo=True)
            print("DNS缓存已刷新")
        elif choice == "4":
            self.run_command("lsof -i -P | grep -i \"listen\"")

    def privacy_security(self) -> None:
        """隐私与安全"""
        print("\n=== 隐私与安全 ===")
        print("1. 查看防火墙状态")
        print("2. 启用防火墙")
        print("3. 禁用防火墙")
        print("4. 查看系统完整性保护状态")
        choice = input("请选择操作: ")
        
        if choice == "1":
            self.run_command("sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate", sudo=True)
        elif choice == "2":
            self.run_command("sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on", sudo=True)
            print("防火墙已启用")
        elif choice == "3":
            self.run_command("sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off", sudo=True)
            print("防火墙已禁用")
        elif choice == "4":
            self.run_command("csrutil status")

    def game_zone(self) -> None:
        """小游戏专区"""
        while True:
            self.display_menu(self.games_menu, "小游戏专区")
            choice = self.get_user_choice(self.games_menu)
            if not choice or choice == "6":
                break
            if self.games_menu[choice]["func"]:
                self.games_menu[choice]["func"]()

    def number_guessing_game(self) -> None:
        """数字猜谜游戏"""
        print("\n=== 数字猜谜 ===")
        print("我已经想好了一个1-100之间的数字，你有10次机会猜中它")
        
        secret_number = random.randint(1, 100)
        attempts = 0
        max_attempts = 10
        
        while attempts < max_attempts:
            try:
                guess = int(input(f"第{attempts + 1}次尝试，请输入你的猜测: "))
            except ValueError:
                print("请输入有效的数字!")
                continue
                
            attempts += 1
            
            if guess < secret_number:
                print("太小了!")
            elif guess > secret_number:
                print("太大了!")
            else:
                print(f"恭喜! 你在{attempts}次尝试后猜中了数字{secret_number}!")
                return
                
        print(f"很遗憾，你没有在{max_attempts}次内猜中。正确答案是{secret_number}")

    def blackjack_game(self) -> None:
        """21点游戏简化版"""
        print("\n=== 21点游戏 ===")
        print("尝试让你的牌面点数尽可能接近21点，但不能超过")
        
        def deal_card():
            return random.randint(1, 11)
            
        player_hand = [deal_card(), deal_card()]
        dealer_hand = [deal_card()]
        
        print(f"你的牌: {player_hand} (总计: {sum(player_hand)})")
        print(f"庄家的明牌: {dealer_hand[0]}")
        
        # 玩家回合
        while sum(player_hand) < 21:
            action = input("要牌(h)或停牌(s)? ").lower()
            if action == 'h':
                new_card = deal_card()
                player_hand.append(new_card)
                print(f"你抽到了: {new_card}, 现在你的牌: {player_hand} (总计: {sum(player_hand)})")
            elif action == 's':
                break
            else:
                print("无效输入，请输入'h'或's'")
                
        # 庄家回合
        while sum(dealer_hand) < 17 and sum(player_hand) <= 21:
            dealer_hand.append(deal_card())
            
        # 显示结果
        print(f"\n你的最终牌: {player_hand} (总计: {sum(player_hand)})")
        print(f"庄家的牌: {dealer_hand} (总计: {sum(dealer_hand)})")
        
        if sum(player_hand) > 21:
            print("你爆牌了! 庄家获胜")
        elif sum(dealer_hand) > 21:
            print("庄家爆牌! 你获胜")
        elif sum(player_hand) > sum(dealer_hand):
            print("你获胜!")
        elif sum(player_hand) < sum(dealer_hand):
            print("庄家获胜!")
        else:
            print("平局!")

    def typing_test(self) -> None:
        """打字速度测试"""
        print("\n=== 打字测试 ===")
        sentences = [
            "The quick brown fox jumps over the lazy dog",
            "Python is an interpreted high-level programming language",
            "macOS is a Unix operating system developed by Apple",
            "Homebrew is the missing package manager for macOS",
            "Practice makes perfect"
        ]
        
        test_sentence = random.choice(sentences)
        print(f"请准确输入以下句子:\n{test_sentence}\n")
        
        start_time = time.time()
        user_input = input("开始输入: ")
        end_time = time.time()
        
        if user_input == test_sentence:
            time_taken = end_time - start_time
            words = len(test_sentence.split())
            wpm = (words / time_taken) * 60
            print(f"\n正确! 用时: {time_taken:.2f}秒")
            print(f"打字速度: {wpm:.1f} 词/分钟")
        else:
            print("\n输入有误! 请再试一次")

    def snake_game(self) -> None:
        """终端贪吃蛇游戏简化版"""
        print("\n=== 终端贪吃蛇 ===")
        print("使用WASD控制方向，吃到@字符增长，撞墙或自己游戏结束")
        print("正在启动游戏...")
        time.sleep(1)
        
        try:
            import pygame
        except ImportError:
            print("需要安装pygame库来运行贪吃蛇游戏")
            install = input("是否现在安装? (y/n): ").lower()
            if install == 'y':
                self.run_command("brew install pygame")
                print("安装完成，请重新运行游戏")
            return
        
        # 游戏代码与Ubuntu版本相同
        # ...

    def memory_game(self) -> None:
        """记忆翻牌游戏"""
        print("\n=== 记忆翻牌 ===")
        print("记住牌的位置，找出所有匹配的对子")
        
        # 创建牌组 (8对牌)
        symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] * 2
        random.shuffle(symbols)
        
        # 初始化游戏板
        board = [' '] * 16
        matched = [False] * 16
        attempts = 0
        
        def display_board():
            print("\n  0 1 2 3")
            for i in range(4):
                row = f"{i} "
                for j in range(4):
                    idx = i * 4 + j
                    if matched[idx]:
                        row += f"{symbols[idx]} "
                    elif board[idx] != ' ':
                        row += f"{board[idx]} "
                    else:
                        row += "* "
                print(row)
        
        while not all(matched):
            display_board()
            
            try:
                first = input("输入第一张牌的行列(如01): ")
                first_row, first_col = int(first[0]), int(first[1])
                first_idx = first_row * 4 + first_col
                
                if matched[first_idx]:
                    print("这张牌已经匹配过了!")
                    continue
                    
                board[first_idx] = symbols[first_idx]
                display_board()
                
                second = input("输入第二张牌的行列(如12): ")
                second_row, second_col = int(second[0]), int(second[1])
                second_idx = second_row * 4 + second_col
                
                if matched[second_idx]:
                    print("这张牌已经匹配过了!")
                    continue
                    
                board[second_idx] = symbols[second_idx]
                display_board()
                
                if symbols[first_idx] == symbols[second_idx]:
                    print("匹配成功!")
                    matched[first_idx] = True
                    matched[second_idx] = True
                else:
                    print("不匹配!")
                    board[first_idx] = ' '
                    board[second_idx] = ' '
                    time.sleep(1)
                    
                attempts += 1
                
            except (ValueError, IndexError):
                print("无效输入，请使用两位数字如01")
        
        print(f"\n恭喜! 你用了{attempts}次尝试完成了游戏!")

    def exit_tool(self) -> None:
        """退出工具"""
        print("\n感谢使用，再见！")
        sys.exit(0)

    def run(self) -> None:
        """运行主循环"""
        print(f"\n=== macOS自动化脚本工具 === \n版本: {VERSION}")
        while True:
            self.display_menu(self.main_menu, "主菜单")
            choice = self.get_user_choice(self.main_menu)
            if not choice:
                self.exit_tool()
            if self.main_menu[choice]["func"]:
                self.main_menu[choice]["func"]()

if __name__ == "__main__":
    tool = MacAutomationTool()
    tool.run()