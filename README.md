# RaveXupo — Telegram controller for Rave on Android

RaveXupo is an experimental Telegram controller for the **Rave Android app** using Appium. It is not yet a verified ready-to-run service: the actual Rave login, room links and chat selectors must be tested on your device/emulator.

## Free hosting: what is realistic?

See [FREE_HOSTING.md](FREE_HOSTING.md) for a comparison of options.

**GitHub Actions is not a 24/7 server.** It runs a temporary job and shuts it down when the job ends. It is useful for code checks and short tests, not for hosting a logged-in Android app permanently.

For a genuinely free setup, the most practical route is to run the Android emulator and bot on your own Windows PC and leave the PC on. Your PC must have enough RAM/CPU for an emulator, virtualization enabled, and must not go to sleep. This has no hosting fee, but it is not cloud hosting.

A free cloud VM is not a dependable solution for this exact project: the bot needs a persistent Android emulator with virtualization, and free cloud services may sleep, lack nested virtualization, or have unsuitable CPU/RAM. For example, Render's free web services sleep after 15 minutes without inbound traffic and are not suitable for this Appium/emulator workload.

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
