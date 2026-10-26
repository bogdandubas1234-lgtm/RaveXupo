#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip openjdk-17-jdk nodejs npm curl unzip
python3 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
sudo npm install -g appium
appium driver install uiautomator2
[ -f .env ] || cp .env.example .env
cat <<'EOF'
Python/Appium dependencies installed.
This script does NOT install Android SDK, create/start an emulator, or sign in to Rave.
Follow README.md, confirm adb devices shows a booted emulator, fill .env,
then start Appium on localhost and run bash start.sh.
EOF
