# RaveXupo — Telegram controller for Rave on Android

This is a starter project, not a verified ready-to-run hosted bot. It controls an already-running Android device/emulator through Appium and receives commands in Telegram.

## Hosting limitation
GitHub stores code but does not keep an Android emulator running 24/7. Hosting requires a machine/service with Android SDK, a booted emulator or connected Android device, and usually KVM/hardware acceleration. Generic GitHub Actions is not a reliable permanent host for this use case.

## Setup
1. Provision an Android host with Java, Android SDK/platform-tools, a system image and a booted AVD. Confirm `adb devices` shows the emulator as `device`.
2. Install Rave from a trusted official source and sign in interactively in the emulator.
3. Enter `rave_bot/`, run `bash setup.sh`, then edit `.env` with `TELEGRAM_TOKEN` and `ALLOWED_USER_ID`.
4. Start Appium on localhost: `appium --address 127.0.0.1 --port 4723`.
5. Run `bash start.sh`.
6. In Telegram, send `/screenshot` and `/dumpui`. Inspect the returned XML and set `RAVE_CHAT_INPUT_ID`, `RAVE_CHAT_SEND_ID`, and `RAVE_CHAT_MESSAGES_XPATH` to real selectors from your Rave version. Restart the bot.

The setup script does not install Android SDK, create an emulator, sign in to Rave, or discover chat selectors. Rave may not support a particular emulator, so the setup and room opening must be tested on the target host.

## Commands
- `/join <room-link>` — open a room link.
- `/say <text>` — send text if selectors are configured.
- `/leave` — stop monitoring.
- `/status` — show state.
- `/screenshot` — send device screenshot.
- `/dumpui` — send Android UI XML.

## Security
- Never commit `.env` or post your Telegram token.
- Only the numeric Telegram user ID in `ALLOWED_USER_ID` can control the bot.
- Keep Appium on localhost; do not expose port 4723 publicly.
- Do not store your Rave password in this project.
