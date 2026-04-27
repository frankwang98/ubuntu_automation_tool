# Windows Automation Tool
# 使用 PowerShell 编写的 Windows 系统自动化管理工具

param(
    [switch]$Silent
)

# 版本信息
$VERSION = "1.0.0"

# 颜色配置
$colors = @{
    "title" = "Cyan"
    "menu" = "White"
    "selected" = "Green"
    "error" = "Red"
    "success" = "Green"
    "info" = "Yellow"
}

function Write-MenuTitle {
    param([string]$Title)
    Write-Host "`n=== $Title ===" -ForegroundColor $colors.title
}

function Write-MenuItem {
    param([string]$Key, [string]$Name)
    Write-Host "$Key. $Name" -ForegroundColor $colors.menu
}

function Write-MenuSelected {
    param([string]$Text)
    Write-Host $Text -ForegroundColor $colors.selected
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "错误: $Message" -ForegroundColor $colors.error
}

function Write-SuccessMsg {
    param([string]$Message)
    Write-Host $Message -ForegroundColor $colors.success
}

function Write-InfoMsg {
    param([string]$Message)
    Write-Host $Message -ForegroundColor $colors.info
}

function Get-UserChoice {
    param([array]$MenuKeys)
    while ($true) {
        $choice = Read-Host "`n请输入数字选择 (q退出)"
        $choice = $choice.Trim()
        if ($choice -eq 'q' -or $choice -eq 'Q') {
            return $null
        }
        if ($MenuKeys -contains $choice) {
            return $choice
        }
        Write-ErrorMsg "无效输入，请重新选择"
    }
}

# ==================== 系统信息 ====================
function Get-SystemInfo {
    Write-MenuTitle "系统信息查询"

    $os = Get-CimInstance -ClassName Win32_OperatingSystem
    $cpu = Get-CimInstance -ClassName Win32_Processor
    $memory = Get-CimInstance -ClassName Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum

    Write-Host "`n--- 操作系统 ---" -ForegroundColor Cyan
    Write-Host "名称: $($os.Caption)"
    Write-Host "版本: $($os.Version)"
    Write-Host "架构: $($os.OSArchitecture)"

    Write-Host "`n--- CPU ---" -ForegroundColor Cyan
    Write-Host "名称: $($cpu.Name)"
    Write-Host "核心数: $($cpu.NumberOfCores)"
    Write-Host "线程数: $($cpu.NumberOfLogicalProcessors)"

    Write-Host "`n--- 内存 ---" -ForegroundColor Cyan
    $totalMemory = [math]::Round($memory.Sum / 1GB, 2)
    $freeMemory = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
    Write-Host "总内存: $totalMemory GB"
    Write-Host "可用内存: $freeMemory GB"

    Write-Host "`n--- 磁盘 ---" -ForegroundColor Cyan
    Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
        $total = [math]::Round($_.Size / 1GB, 2)
        $free = [math]::Round($_.FreeSpace / 1GB, 2)
        Write-Host "$($_.DeviceID) 总容量: $total GB, 可用: $free GB"
    }

    Write-Host "`n--- 网络 ---" -ForegroundColor Cyan
    $adapters = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' }
    foreach ($adapter in $adapters) {
        $ip = Get-NetIPAddress -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue
        Write-Host "$($adapter.Name): $($ip.IPAddress)"
    }
}

# ==================== 系统更新 ====================
function Update-System {
    Write-MenuTitle "系统更新"

    Write-InfoMsg "检查 Windows 更新..."

    # 检查是否安装 Windows Update 模块
    $wuModule = Get-Module -ListAvailable -Name PSWindowsUpdate
    if (-not $wuModule) {
        Write-InfoMsg "需要安装 PSWindowsUpdate 模块..."
        $install = Read-Host "是否安装? (y/n)"
        if ($install -eq 'y' -or $install -eq 'Y') {
            try {
                Install-Module -Name PSWindowsUpdate -Force -Scope CurrentUser
                Write-SuccessMsg "安装完成"
            } catch {
                Write-ErrorMsg "安装失败: $_"
                return
            }
        } else {
            Write-InfoMsg "跳过安装，请在管理员模式下运行以下命令安装:"
            Write-Host "Install-Module -Name PSWindowsUpdate -Force -Scope CurrentUser" -ForegroundColor Yellow
            return
        }
    }

    Write-Host "`n可用更新:" -ForegroundColor Cyan
    Get-WindowsUpdate -Category "Windows Updates" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "  - $($_.Title)"
    }

    $confirm = Read-Host "`n是否安装更新? (y/n)"
    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        Write-InfoMsg "正在安装更新..."
        Install-WindowsUpdate -Category "Windows Updates" -AcceptAll -AutoReboot:$false -ErrorAction SilentlyContinue
        Write-SuccessMsg "更新完成"
    }
}

# ==================== 系统清理 ====================
function Clear-System {
    Write-MenuTitle "系统清理"

    $tasks = @(
        @{Name="清理临时文件"; Action={
            Write-InfoMsg "清理临时文件..."
            Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
            Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
            Write-SuccessMsg "清理完成"
        }},
        @{Name="清空回收站"; Action={
            Write-InfoMsg "清空回收站...
            Clear-RecycleBin -Force -ErrorAction SilentlyContinue
            Write-SuccessMsg "回收站已清空"
        }},
        @{Name="清理 Windows 更新缓存"; Action={
            Write-InfoMsg "清理更新缓存..."
            Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue
            Remove-Item -Path "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
            Start-Service -Name wuauserv -ErrorAction SilentlyContinue
            Write-SuccessMsg "更新缓存已清理"
        }},
        @{Name="清理浏览器缓存"; Action={
            Write-InfoMsg "清理浏览器缓存..."
            $browserPaths = @(
                "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache",
                "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\Cache",
                "$env:LOCALAPPDATA\Mozilla\Firefox\Profiles\*\cache2"
            )
            foreach ($path in $browserPaths) {
                Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
            }
            Write-SuccessMsg "浏览器缓存已清理"
        }}
    )

    foreach ($i in 0..($tasks.Count-1)) {
        Write-MenuItem ($i+1) $tasks[$i].Name
    }
    Write-MenuItem "0" "返回主菜单"

    $choice = Get-UserChoice -MenuKeys (0..$tasks.Count)
    if ($null -eq $choice) { return }
    if ($choice -eq "0") { return }

    $taskIndex = [int]$choice - 1
    & $tasks[$taskIndex].Action

    Write-Host "`n按回车继续..." -ForegroundColor Gray
    Read-Host
}

# ==================== 安装软件 ====================
function Install-Software {
    Write-MenuTitle "安装常用软件"

    $apps = @(
        @{Name="Git"; Id="Git.Git"},
        @{Name="VS Code"; Id="Microsoft.VisualStudioCode"},
        @{Name="Node.js"; Id="OpenJS.NodeJS.LTS"},
        @{Name="Python"; Id="Python.Python.3.11"},
        @{Name="Docker Desktop"; Id="Docker.DockerDesktop"},
        @{Name="Chrome"; Id="Google.Chrome"},
        @{Name="Edge"; Id="Microsoft.Edge"},
        @{Name="7-Zip"; Id="7zip.7zip"},
        @{Name="Notepad++"; Id="Notepad++.Notepad++"},
        @{Name="返回主菜单"; Id=""}
    )

    foreach ($i in 0..($apps.Count-1)) {
        Write-MenuItem ($i+1) $apps[$i].Name
    }

    $choice = Get-UserChoice -MenuKeys (1..$apps.Count)
    if ($null -eq $choice) { return }

    $appIndex = [int]$choice - 1
    if ($appIndex -ge $apps.Count - 1) { return }

    $app = $apps[$appIndex]

    Write-InfoMsg "正在安装 $($app.Name)..."
    try {
        winget install --id $app.Id --silent --accept-package-agreements --accept-source-agreements
        Write-SuccessMsg "$($app.Name) 安装完成"
    } catch {
        Write-ErrorMsg "安装失败: $_"
    }

    Write-Host "`n按回车继续..." -ForegroundColor Gray
    Read-Host
}

# ==================== Docker 管理 ====================
function Manage-Docker {
    Write-MenuTitle "Docker 管理"

    $dockerStatus = Get-Service -Name "com.docker.service" -ErrorAction SilentlyContinue
    $isRunning = $dockerStatus -and $dockerStatus.Status -eq 'Running'

    Write-Host "`nDocker 状态: " -NoNewline
    if ($isRunning) {
        Write-SuccessMsg "运行中"
    } else {
        Write-ErrorMsg "未运行"
    }

    $submenu = @(
        @{Name="启动 Docker"; Action={
            Start-Service -Name "com.docker.service" -ErrorAction SilentlyContinue
            Start-Process "dockerd" -ErrorAction SilentlyContinue
            Write-SuccessMsg "Docker 已启动"
        }},
        @{Name="停止 Docker"; Action={
            Stop-Service -Name "com.docker.service" -Force -ErrorAction SilentlyContinue
            Write-SuccessMsg "Docker 已停止"
        }},
        @{Name="查看容器"; Action={
            docker ps -a
        }},
        @{Name="查看镜像"; Action={
            docker images
        }},
        @{Name="清理无用容器/镜像"; Action={
            Write-InfoMsg "清理停止的容器..."
            docker container prune -f
            Write-InfoMsg "清理悬空镜像..."
            docker image prune -f
            Write-SuccessMsg "清理完成"
        }},
        @{Name="返回主菜单"; Id=""}
    )

    foreach ($i in 0..($submenu.Count-1)) {
        Write-MenuItem ($i+1) $submenu[$i].Name
    }

    $choice = Get-UserChoice -MenuKeys (1..$submenu.Count)
    if ($null -eq $choice) { return }

    $index = [int]$choice - 1
    if ($index -ge $submenu.Count - 1) { return }

    & $submenu[$index].Action

    Write-Host "`n按回车继续..." -ForegroundColor Gray
    Read-Host
}

# ==================== 网络工具 ====================
function Show-NetworkTools {
    Write-MenuTitle "网络工具"

    $tools = @(
        @{Name="测试网络连接"; Action={
            Write-Host "`n请输入要测试的地址 (直接回车测试百度):" -ForegroundColor Yellow
            $target = Read-Host
            if ([string]::IsNullOrWhiteSpace($target)) {
                $target = "www.baidu.com"
            }
            Test-Connection -ComputerName $target -Count 4
        }},
        @{Name="查看网络配置"; Action={
            Get-NetIPConfiguration | Select-Object InterfaceAlias, IPv4Address, IPv4DefaultGateway | Format-List
        }},
        @{Name="查看端口占用"; Action={
            Write-Host "`n请输入要查看的端口 (如 80):" -ForegroundColor Yellow
            $port = Read-Host
            if ($port -match '^\d+$') {
                Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Format-Table -AutoSize
            }
        }},
        @{Name="刷新 DNS 缓存"; Action={
            Clear-DnsClientCache
            Write-SuccessMsg "DNS 缓存已刷新"
        }},
        @{Name="返回主菜单"; Id=""}
    )

    foreach ($i in 0..($tools.Count-1)) {
        Write-MenuItem ($i+1) $tools[$i].Name
    }

    $choice = Get-UserChoice -MenuKeys (1..$tools.Count)
    if ($null -eq $choice) { return }

    $index = [int]$choice - 1
    if ($index -ge $tools.Count - 1) { return }

    & $tools[$index].Action

    Write-Host "`n按回车继续..." -ForegroundColor Gray
    Read-Host
}

# ==================== 小游戏 ====================
function Start-GameZone {
    Write-MenuTitle "小游戏专区"

    $games = @(
        @{Name="数字猜谜"; Func={ Start-NumberGuessingGame }},
        @{Name="21点游戏"; Func={ Start-BlackjackGame }},
        @{Name="返回主菜单"; Func={ return }}
    )

    foreach ($i in 0..($games.Count-1)) {
        Write-MenuItem ($i+1) $games[$i].Name
    }

    $choice = Get-UserChoice -MenuKeys (1..$games.Count)
    if ($null -eq $choice) { return }

    $index = [int]$choice - 1
    & $games[$index].Func

    Write-Host "`n按回车继续..." -ForegroundColor Gray
    Read-Host
}

function Start-NumberGuessingGame {
    Write-MenuTitle "数字猜谜游戏"

    $target = Get-Random -Minimum 1 -Maximum 100
    $attempts = 0
    $maxAttempts = 7

    Write-Host "我已经想好了一个 1-100 之间的数字" -ForegroundColor Cyan
    Write-Host "你有 $maxAttempts 次机会猜测`n" -ForegroundColor Cyan

    while ($attempts -lt $maxAttempts) {
        $guess = Read-Host "请输入你的猜测 (剩余 $($maxAttempts - $attempts) 次)"
        if ($guess -match '^\d+$') {
            $attempts++
            if ($guess -eq $target) {
                Write-SuccessMsg "恭喜你! 猜对了! 数字是 $target"
                Write-Host "你用了 $attempts 次猜测" -ForegroundColor Green
                return
            } elseif ($guess -lt $target) {
                Write-Host "太小了!" -ForegroundColor Yellow
            } else {
                Write-Host "太大了!" -ForegroundColor Yellow
            }
        } else {
            Write-ErrorMsg "请输入有效的数字"
        }
    }

    Write-ErrorMsg "游戏结束! 正确答案是 $target"
}

function Start-BlackjackGame {
    Write-MenuTitle "21点游戏"

    function Get-CardValue {
        param([string]$Card)
        if ($Card -match 'J|Q|K') { return 10 }
        if ($Card -match 'A') { return 11 }
        return [int]$Card
    }

    function Get-RandomCard {
        $suits = @('♠', '♥', '♦', '♣')
        $values = @('2','3','4','5','6','7','8','9','10','J','Q','K','A')
        return @{
            Suit = $suits | Get-Random
            Value = $values | Get-Random
        }
    }

    $playerCards = @()
    $dealerCards = @()

    # 发牌
    $playerCards += Get-RandomCard
    $dealerCards += Get-RandomCard
    $playerCards += Get-RandomCard
    $dealerCards += Get-RandomCard

    Write-Host "`n你的手牌: " -NoNewline
    foreach ($card in $playerCards) {
        Write-Host "$($card.Value)$($card.Suit) " -NoNewline -ForegroundColor Green
    }

    Write-Host "`n庄家的明牌: " -NoNewline
    Write-Host "$($dealerCards[0].Value)$($dealerCards[0].Suit)" -ForegroundColor Red

    # 玩家要牌
    $playerTurn = $true
    while ($playerTurn) {
        $playerTotal = 0
        $aces = 0
        foreach ($card in $playerCards) {
            $val = Get-CardValue -Card $card.Value
            $playerTotal += $val
            if ($card.Value -eq 'A') { $aces++ }
        }
        while ($playerTotal -gt 21 -and $aces -gt 0) {
            $playerTotal -= 10
            $aces--
        }

        Write-Host "`n你的总分: $playerTotal" -ForegroundColor Cyan
        $action = Read-Host "要牌(h) 还是 停牌(s)?"
        if ($action -eq 'h' -or $action -eq 'H') {
            $playerCards += Get-RandomCard
            $playerTotal = 0
            $aces = 0
            foreach ($card in $playerCards) {
                $val = Get-CardValue -Card $card.Value
                $playerTotal += $val
                if ($card.Value -eq 'A') { $aces++ }
            }
            while ($playerTotal -gt 21 -and $aces -gt 0) {
                $playerTotal -= 10
                $aces--
            }
            Write-Host "你的手牌: " -NoNewline
            foreach ($card in $playerCards) {
                Write-Host "$($card.Value)$($card.Suit) " -NoNewline -ForegroundColor Green
            }
            if ($playerTotal -gt 21) {
                Write-Host "`n" -NoNewline
                Write-ErrorMsg "爆牌了! 你输了"
                return
            }
        } else {
            $playerTurn = $false
        }
    }

    # 庄家回合
    Write-Host "`n庄家的手牌: " -NoNewline
    foreach ($card in $dealerCards) {
        Write-Host "$($card.Value)$($card.Suit) " -NoNewline -ForegroundColor Red
    }

    while ($true) {
        $dealerTotal = 0
        $aces = 0
        foreach ($card in $dealerCards) {
            $val = Get-CardValue -Card $card.Value
            $dealerTotal += $val
            if ($card.Value -eq 'A') { $aces++ }
        }
        while ($dealerTotal -gt 21 -and $aces -gt 0) {
            $dealerTotal -= 10
            $aces--
        }
        if ($dealerTotal -ge 17) { break }
        $dealerCards += Get-RandomCard
        Write-Host "$($dealerCards[-1].Value)$($dealerCards[-1].Suit) " -NoNewline -ForegroundColor Red
    }

    Write-Host "`n庄家总分: $dealerTotal" -ForegroundColor Cyan

    # 判断胜负
    $playerTotal = 0
    $aces = 0
    foreach ($card in $playerCards) {
        $val = Get-CardValue -Card $card.Value
        $playerTotal += $val
        if ($card.Value -eq 'A') { $aces++ }
    }
    while ($playerTotal -gt 21 -and $aces -gt 0) {
        $playerTotal -= 10
        $aces--
    }

    if ($dealerTotal -gt 21) {
        Write-SuccessMsg "庄家爆牌! 你赢了!"
    } elseif ($playerTotal -gt $dealerTotal) {
        Write-SuccessMsg "你赢了! ($playerTotal vs $dealerTotal)"
    } elseif ($playerTotal -lt $dealerTotal) {
        Write-ErrorMsg "你输了! ($playerTotal vs $dealerTotal)"
    } else {
        Write-InfoMsg "平局! ($playerTotal vs $dealerTotal)"
    }
}

# ==================== 退出 ====================
function Exit-Tool {
    Write-Host "`n感谢使用! 再见!" -ForegroundColor Green
    exit 0
}

# ==================== 主菜单 ====================
$mainMenu = @(
    @{Name="系统信息查询"; Func={ Get-SystemInfo }},
    @{Name="系统更新"; Func={ Update-System }},
    @{Name="系统清理"; Func={ Clear-System }},
    @{Name="安装软件"; Func={ Install-Software }},
    @{Name="Docker管理"; Func={ Manage-Docker }},
    @{Name="网络工具"; Func={ Show-NetworkTools }},
    @{Name="小游戏专区"; Func={ Start-GameZone }},
    @{Name="退出"; Func={ Exit-Tool }}
)

function Show-MainMenu {
    param([bool]$FirstRun = $false)

    if ($FirstRun) {
        Write-Host ""
        Write-Host "======================================" -ForegroundColor Cyan
        Write-Host "     Windows 自动化工具 v$VERSION" -ForegroundColor Cyan
        Write-Host "======================================" -ForegroundColor Cyan
        Write-Host ""
    }

    Write-MenuTitle "主菜单"
    foreach ($i in 0..($mainMenu.Count-1)) {
        Write-MenuItem ($i+1) $mainMenu[$i].Name
    }
}

# ==================== 主循环 ====================
function Start-MainLoop {
    $firstRun = $true

    while ($true) {
        Show-MainMenu -FirstRun $firstRun
        $firstRun = $false

        $keys = 1..$mainMenu.Count
        $choice = Get-UserChoice -MenuKeys $keys

        if ($null -eq $choice) {
            Exit-Tool
        }

        $index = [int]$choice - 1
        & $mainMenu[$index].Func
    }
}

# 启动主循环
Start-MainLoop