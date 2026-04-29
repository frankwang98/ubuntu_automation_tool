#!/usr/bin/env python3
import os
import subprocess
import platform
import time
import sys
import random
import readline
import requests
from datetime import datetime
from typing import Dict, Optional

VERSION = "1.0.0 - " + datetime.now().strftime("%Y-%m-%d")

class UbuntuAutomationTool:
    def __init__(self):
        self.main_menu = {
            "1": {"name": "系统信息查询", "func": self.system_info},
            "2": {"name": "系统更新", "func": self.system_update},
            "3": {"name": "系统清理", "func": self.system_clean},
            "4": {"name": "安装基础工具", "func": self.install_basic_tools},
            "5": {"name": "Docker管理", "func": self.docker_management},
            "6": {"name": "测试脚本", "func": self.test_scripts},
            "7": {"name": "应用市场", "func": self.app_market},
            "8": {"name": "网络工具", "func": self.network_tools},
            "9": {"name": "小游戏专区", "func": self.game_zone},
            "10": {"name": "退出", "func": self.exit_tool}
        }
        
        self.docker_submenu = {
            "1": {"name": "容器管理", "func": self.docker_container_management},
            "2": {"name": "镜像管理", "func": self.docker_image_management},
            "3": {"name": "清理无用容器/镜像", "func": self.docker_cleanup},
            "4": {"name": "返回主菜单", "func": None}
        }
        
        self.test_scripts_menu = {
            "1": {"name": "运行磁盘测试", "func": self.run_disk_test},
            "2": {"name": "运行CPU测试", "func": self.run_cpu_test},
            "3": {"name": "运行内存测试", "func": self.run_memory_test},
            "4": {"name": "自定义脚本", "func": self.custom_script},
            "5": {"name": "返回主菜单", "func": None}
        }
        
        self.recommended_apps = {
            "1": {"name": "htop (系统监控)", "command": "sudo apt install -y htop"},
            "2": {"name": "neofetch (系统信息)", "command": "sudo apt install -y neofetch"},
            "3": {"name": "tmux (终端复用)", "command": "sudo apt install -y tmux"},
            "4": {"name": "ncdu (磁盘分析)", "command": "sudo apt install -y ncdu"},
            "5": {"name": "bat (更好的cat)", "command": "sudo apt install -y bat"},
            "6": {"name": "返回主菜单", "command": None}
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
        print(f"系统类型: {platform.system()}")
        print(f"系统版本: {platform.version()}")
        print(f"系统架构: {platform.machine()}")
        print(f"内核版本: {platform.release()}")
        print(f"主机名: {platform.node()}")
        self.run_command("uptime")
        self.run_command("free -h")
        self.run_command("df -h")

    def system_update(self) -> None:
        """系统更新"""
        print("\n正在更新系统...")
        self.run_command("apt update", sudo=True)
        self.run_command("apt upgrade -y", sudo=True)
        self.run_command("apt autoremove -y", sudo=True)
        print("系统更新完成")

    def system_clean(self) -> None:
        """系统清理"""
        print("\n正在清理系统...")
        self.run_command("apt autoremove -y", sudo=True)
        self.run_command("apt clean", sudo=True)
        # self.run_command("rm -rf ~/.cache/*", sudo=False)
        print("系统清理完成")

    def install_basic_tools(self) -> None:
        """安装基础工具"""
        tools = [
            "curl", "wget", "git", "vim", "tmux", "htop",
            "net-tools", "tree", "unzip", "jq", "rsync",
            "build-essential", "cmake", "g++", "sysbench"
        ]
        print("\n正在安装基础工具...")
        self.run_command(f"apt install -y {' '.join(tools)}", sudo=True)
        print("基础工具安装完成")

    def docker_management(self) -> None:
        """Docker管理主菜单"""
        while True:
            self.display_menu(self.docker_submenu, "Docker管理")
            choice = self.get_user_choice(self.docker_submenu)
            if not choice or choice == "4":
                break
            if self.docker_submenu[choice]["func"]:
                self.docker_submenu[choice]["func"]()

    def docker_container_management(self) -> None:
        """Docker容器管理"""
        print("\n=== Docker容器管理 ===")
        print("1. 列出运行中的容器")
        print("2. 列出所有容器")
        print("3. 启动容器")
        print("4. 停止容器")
        print("5. 删除容器")
        choice = input("请选择操作: ")
        
        if choice == "1":
            self.run_command("docker ps")
        elif choice == "2":
            self.run_command("docker ps -a")
        elif choice == "3":
            container = input("输入要启动的容器ID或名称: ")
            self.run_command(f"docker start {container}")
        elif choice == "4":
            container = input("输入要停止的容器ID或名称: ")
            self.run_command(f"docker stop {container}")
        elif choice == "5":
            container = input("输入要删除的容器ID或名称: ")
            self.run_command(f"docker rm {container}")

    def docker_image_management(self) -> None:
        """Docker镜像管理"""
        print("\n=== Docker镜像管理 ===")
        print("1. 列出本地镜像")
        print("2. 拉取镜像")
        print("3. 删除镜像")
        choice = input("请选择操作: ")
        
        if choice == "1":
            self.run_command("docker images")
        elif choice == "2":
            image = input("输入要拉取的镜像名称 (如ubuntu:latest): ")
            self.run_command(f"docker pull {image}")
        elif choice == "3":
            image = input("输入要删除的镜像ID或名称: ")
            self.run_command(f"docker rmi {image}")

    def docker_cleanup(self) -> None:
        """清理无用的Docker资源"""
        print("\n正在清理无用的Docker资源...")
        self.run_command("docker system prune -f")
        print("Docker清理完成")

    def test_scripts(self) -> None:
        """测试脚本"""
        while True:
            self.display_menu(self.test_scripts_menu, "测试脚本")
            choice = self.get_user_choice(self.test_scripts_menu)
            if not choice or choice == "5":
                break
            if self.test_scripts_menu[choice]["func"]:
                self.test_scripts_menu[choice]["func"]()

    def run_disk_test(self) -> None:
        """运行磁盘测试"""
        print("\n正在运行磁盘测试...")
        self.run_command("dd if=/dev/zero of=./testfile bs=1M count=1024 conv=fdatasync")
        self.run_command("rm -f ./testfile")
        print("磁盘测试完成")

    def run_cpu_test(self) -> None:
        """运行CPU测试"""
        print("\n正在运行CPU测试...")
        self.run_command("sysbench cpu --cpu-max-prime=20000 run")
        print("CPU测试完成")

    def run_memory_test(self) -> None:
        """运行内存测试"""
        print("\n正在运行内存测试...")
        self.run_command("sysbench memory run")
        print("内存测试完成")

    def custom_script(self) -> None:
        """运行自定义脚本"""
        script = input("输入要执行的命令或脚本路径: ")
        self.run_command(script)

    def app_market(self) -> None:
        """应用市场"""
        while True:
            print("\n=== 推荐应用 ===")
            for key, value in self.recommended_apps.items():
                print(f"{key}. {value['name']}")
            
            choice = input("请选择要安装的应用 (q返回): ").strip()
            if choice.lower() == 'q':
                break
            if choice in self.recommended_apps and self.recommended_apps[choice]["command"]:
                self.run_command(self.recommended_apps[choice]["command"], sudo=True)

    def network_tools(self) -> None:
        """网络工具"""
        print("\n=== 网络工具 ===")
        print("1. 检查网络连接")
        print("2. 查看网络接口")
        print("3. 查看网络连接状态")
        print("4. 查看端口占用")
        choice = input("请选择操作: ")
        
        if choice == "1":
            self.run_command("ping -c 4 baidu.com")
        elif choice == "2":
            self.run_command("ip a")
        elif choice == "3":
            self.run_command("iwconfig")
        elif choice == "4":
            self.run_command("netstat -tulnp")

    
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
            "Ubuntu is a Linux distribution based on Debian",
            "Open source software is changing the world",
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
        import time
        time.sleep(1)
        
        try:
            import pygame
        except ImportError:
            print("需要安装pygame库来运行贪吃蛇游戏")
            install = input("是否现在安装? (y/n): ").lower()
            if install == 'y':
                self.run_command("sudo apt install -y python3-pygame", sudo=True)
                print("安装完成，请重新运行游戏")
            return
        
        # game loop and game functions here
        import pygame
        import time
        import random
        
        pygame.init()
        
        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (213, 50, 80)
        green = (0, 255, 0)
        
        dis_width = 600
        dis_height = 400
        dis = pygame.display.set_mode((dis_width, dis_height))
        pygame.display.set_caption('贪吃蛇游戏')
        
        clock = pygame.time.Clock()
        snake_block = 10
        snake_speed = 15
        
        font_style = pygame.font.SysFont(None, 30)
        
        def message(msg, color):
            mesg = font_style.render(msg, True, color)
            dis.blit(mesg, [dis_width / 6, dis_height / 3])
        
        def gameLoop():
            game_over = False
            game_close = False
            
            x1 = dis_width / 2
            y1 = dis_height / 2
            
            x1_change = 0
            y1_change = 0
            
            snake_List = []
            Length_of_snake = 1
            
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            
            while not game_over:
                
                while game_close == True:
                    dis.fill(black)
                    message("游戏结束! 按Q-退出或C-再玩一次", red)
                    pygame.display.update()
                    
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                game_over = True
                                game_close = False
                            if event.key == pygame.K_c:
                                gameLoop()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            x1_change = -snake_block
                            y1_change = 0
                        elif event.key == pygame.K_RIGHT:
                            x1_change = snake_block
                            y1_change = 0
                        elif event.key == pygame.K_UP:
                            y1_change = -snake_block
                            x1_change = 0
                        elif event.key == pygame.K_DOWN:
                            y1_change = snake_block
                            x1_change = 0
                
                if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                    game_close = True
                x1 += x1_change
                y1 += y1_change
                dis.fill(black)
                pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
                snake_Head = []
                snake_Head.append(x1)
                snake_Head.append(y1)
                snake_List.append(snake_Head)
                if len(snake_List) > Length_of_snake:
                    del snake_List[0]
                
                for x in snake_List[:-1]:
                    if x == snake_Head:
                        game_close = True
                
                for x in snake_List:
                    pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])
                
                pygame.display.update()
                
                if x1 == foodx and y1 == foody:
                    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                    Length_of_snake += 1
                
                clock.tick(snake_speed)
            
            pygame.quit()
            quit()
        
        gameLoop()

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
        print(f"\n=== Ubuntu自动化脚本工具 === \n版本: {VERSION}")
        while True:
            self.display_menu(self.main_menu, "主菜单")
            choice = self.get_user_choice(self.main_menu)
            if not choice:
                self.exit_tool()
            if self.main_menu[choice]["func"]:
                self.main_menu[choice]["func"]()

if __name__ == "__main__":
    tool = UbuntuAutomationTool()
    tool.run()
