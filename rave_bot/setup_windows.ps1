$ErrorActionPreference = "Stop"
$botDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Require-Command([string]$Name, [string]$InstallHint) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "$Name was not found in PATH. $InstallHint"
    }
}

Require-Command "python" "Install Python 3.10+ and enable Add Python to PATH."
Require-Command "npm" "Install Node.js LTS, then reopen PowerShell."
Require-Command "adb" "Install Android SDK Platform-Tools in Android Studio and add platform-tools to PATH."
Require-Command "emulator" "Install Android Emulator in Android Studio and add the SDK emulator folder to PATH."

Push-Location $botDir
try {
    python -m venv venv
    & ".\venv\Scripts\python.exe" -m pip install --upgrade pip
    & ".\venv\Scripts\python.exe" -m pip install -r requirements.txt

    $appium = Get-Command appium -ErrorAction SilentlyContinue
    if (-not $appium) {
        npm install --global appium
    }
    appium driver install uiautomator2

    if (-not (Test-Path ".env")) {
        Copy-Item ".env.example" ".env"
        Write-Host "Created rave_bot\.env. Edit it and add TELEGRAM_TOKEN and ALLOWED_USER_ID."
    }

    Write-Host ""
    Write-Host "Setup installed Python/Appium dependencies."
    Write-Host "Android Studio, the emulator, Rave installation and Rave sign-in are manual steps."
    Write-Host "Read the Windows quick-start section in the repository README."
}
finally {
    Pop-Location
}
