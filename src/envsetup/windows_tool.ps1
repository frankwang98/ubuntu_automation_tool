# Simple test version - no Chinese

$VERSION = "1.0.0"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "     Windows Automation Tool v$VERSION" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. System Info"
Write-Host "2. Test Ping"
Write-Host "3. Disk Usage"
Write-Host "4. Exit"

while ($true) {
    $choice = Read-Host "`nSelect (1-4)"

    switch ($choice) {
        "1" {
            Write-Host "`n--- System ---" -ForegroundColor Cyan
            Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, OSArchitecture | Format-List
        }
        "2" {
            $target = Read-Host "Enter hostname or press Enter for localhost"
            if ([string]::IsNullOrWhiteSpace($target)) { $target = "localhost" }
            Test-Connection -ComputerName $target -Count 2
        }
        "3" {
            Write-Host "`n--- Disks ---" -ForegroundColor Cyan
            Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | Select-Object DeviceID, @{N="Size(GB)";E={[math]::Round($_.Size/1GB,2)}}, @{N="Free(GB)";E={[math]::Round($_.FreeSpace/1GB,2)}} | Format-Table -AutoSize
        }
        "4" {
            Write-Host "Bye!" -ForegroundColor Green
            exit 0
        }
    }
}