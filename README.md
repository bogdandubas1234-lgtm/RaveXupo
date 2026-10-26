# RaveXupo — Telegram controller for Rave on Android

RaveXupo is an experimental Telegram controller for the **Rave Android app** using Appium. It is not yet a verified ready-to-run service: the actual Rave login, room links and chat selectors must be tested on your device/emulator.

## Can I host it from my phone for free, 24/7?

**Not with a currently verified, reliable setup.** RaveXupo needs a persistent Android device/emulator running Rave, plus Appium and the Python Telegram controller. A free Linux VM alone does not guarantee that a compatible Android emulator can run there.

See [FREE_HOSTING.md](FREE_HOSTING.md) for a realistic comparison and a phone-only checklist for investigating Oracle Cloud Always Free. OCI is an experiment, not a guaranteed deployment: ARM VM compatibility, emulator acceleration, available capacity, and signup verification are potential blockers. Do not enable paid resources just to test.

GitHub Actions is not a 24/7 server. It runs temporary jobs and shuts them down when each job ends. GitHub Codespaces also has limited free compute and is not a guaranteed always-on host. Termux can run Python on Android, but it cannot straightforwardly control the same phone's Rave UI through this project's current Appium setup without a compatible device/ADB or accessibility bridge.

## Windows quick start

1. Install **Node.js LTS** and **Android Studio** on the Windows PC.
2. In Android Studio > SDK Manager, install Android SDK Platform-Tools and Android Emulator. In Device Manager, create and boot an Android virtual device. Prefer a Google Play image if available.
3. Install Rave in the emulator from a trusted official source and sign in manually. Do not put your Rave password in this repository.
4. Install Python 3.10+ and ensure Python, npm, adb and emulator are available in PATH.
5. Open PowerShell in the repository and run:
   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\rave_bot\setup_windows.ps1
   ```
6. Copy `rave_bot\.env.example` to `rave_bot\.env`. Fill `TELEGRAM_TOKEN` and `ALLOWED_USER_ID` privately.
7. Run ` .\rave_bot\start_windows.ps1 -AvdName "YOUR_AVD_NAME" ` (replace with the AVD name shown in Android Studio Device Manager).
8. In Telegram, send `/screenshot` and `/dumpui`. The chat selectors are not known in advance; inspect the returned XML and set `RAVE_CHAT_INPUT_ID`, `RAVE_CHAT_SEND_ID`, and `RAVE_CHAT_MESSAGES_XPATH` in `.env`, then restart.

### Keep the PC awake

In Windows Settings > System > Power, set sleep to **Never while plugged in**. Keep the emulator, Appium and bot running. If the PC restarts or loses internet, you may need to start the script again.

## Commands

- `/join <room-link>` — open a room link.
- `/say <text>` — send a message if chat selectors are configured.
- `/leave` — stop monitoring.
- `/status` — show state.
- `/screenshot` — send a device screenshot.
- `/dumpui` — send Android UI XML to help configure selectors.

## Important limitations

- The scripts do not install or authenticate Rave automatically.
- The configured Android package name and deep-link behaviour may differ from the current Rave version.
- Chat reading and sending will not work until real selectors are configured and tested.
- The syntax-check workflow only checks Python syntax; it does not prove Rave automation works.

## Security

- Never commit `.env` or share your Telegram bot token.
- Only the numeric Telegram user ID in `ALLOWED_USER_ID` can control the bot.
- Keep Appium on localhost; do not expose port 4723 to the public internet.
- Do not store your Rave password in this project.
