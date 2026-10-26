param(
    [Parameter(Mandatory = $false)]
    [string]$AvdName = ""
)
$ErrorActionPreference = "Stop"
$botDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $botDir
try {
    if (-not (Test-Path ".env")) {
        throw "Missing .env. Run setup_windows.ps1 and fill in TELEGRAM_TOKEN and ALLOWED_USER_ID first."
    }

    $devices = (& adb devices) -join "`n"
    if ($devices -notmatch "(?m)^emulator-\d+\s+device$") {
        if ([string]::IsNullOrWhiteSpace($AvdName)) {
            throw "No booted Android emulator found. Start one in Android Studio Device Manager, or run: .\start_windows.ps1 -AvdName 'YOUR_AVD_NAME'"
        }
        Start-Process -FilePath "emulator" -ArgumentList @("-avd", $AvdName, "-no-snapshot-save", "-no-audio") | Out-Null
        Write-Host "Starting emulator '$AvdName'..."
        $ready = $false
        for ($i = 0; $i -lt 60; $i++) {
            Start-Sleep -Seconds 5
            $devices = (& adb devices) -join "`n"
            if ($devices -match "(?m)^emulator-\d+\s+device$") {
                $ready = $true
                break
            }
        }
        if (-not $ready) {
            throw "Emulator did not become ready in 5 minutes. Start it manually in Android Studio and retry."
        }
    }

    $appiumReady = $false
    try {
        $status = Invoke-RestMethod -Uri "http://127.0.0.1:4723/status" -TimeoutSec 2
        $appiumReady = $true
    } catch {}

    if (-not $appiumReady) {
        Start-Process -FilePath "appium" -ArgumentList @("--address", "127.0.0.1", "--port", "4723") -WindowStyle Hidden | Out-Null
        Start-Sleep -Seconds 8
        try {
            $null = Invoke-RestMethod -Uri "http://127.0.0.1:4723/status" -TimeoutSec 3
            $appiumReady = $true
        } catch {}
    }
    if (-not $appiumReady) {
        throw "Appium did not start. Run 'appium --address 127.0.0.1 --port 4723' manually and check its error."
    }

    if (-not (Test-Path ".\venv\Scripts\python.exe")) {
        throw "Python environment missing. Run .\setup_windows.ps1 first."
    }
    Write-Host "Starting RaveXupo bot. Keep this PC awake and this process running."
    & ".\venv\Scripts\python.exe" ".\controller.py"
}
finally {
    Pop-Location
}
