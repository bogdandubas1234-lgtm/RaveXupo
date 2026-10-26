# Free hosting for RaveXupo (phone-only setup)

## Honest answer first

RaveXupo currently automates the **Rave Android app** through Appium. A working deployment therefore needs all of these at once:

- a persistent Android device or emulator;
- Rave installed and manually signed in;
- Appium and the Python Telegram controller;
- stable access to the device UI, plus configured selectors for the current Rave version.

A free Linux server is **not automatically an Android emulator host**. No cloud option has been verified end-to-end for this repository, so this guide does not promise free 24/7 operation.

## Cloud option to test Appium: SpawnDroid

[SpawnDroid](https://spawndroid.io/) provides Android 12–16 sessions on ARM64 servers and a hosted Appium endpoint. Its current Free plan advertises one parallel runner without a time cap and without a credit card.

This is a useful **compatibility experiment**, not a verified 24/7 host:

- Each session runs on an isolated Android container and is destroyed when the session ends.
- The service terms say sessions may be reaped when idle and uninterrupted availability is not guaranteed.
- Rave must be installed and signed in inside the cloud session. A new session may not preserve that login or app state.
- The current RaveXupo code expects its own Appium/device setup. It has not yet been adapted or tested against SpawnDroid's hosted endpoint.
- Before changing the bot, verify that you can install and sign in to Rave in a session and that the session stays alive for the period you need.

Start here:
- [SpawnDroid](https://spawndroid.io/)
- [SpawnDroid help and Appium guides](https://spawndroid.io/help/)
- [SpawnDroid terms](https://spawndroid.io/terms/)

### Phone-only preflight checklist

1. Open SpawnDroid in your phone browser and create a free workspace if eligible.
2. Start a manual Android session and check whether Rave can be installed and opened.
3. Sign in manually; never send your Rave password or session credentials to anyone.
4. Check whether the session stays alive while idle and whether you can create a fresh session after it ends.
5. Only after those checks should we adapt RaveXupo to the hosted Appium URL. Do not assume this provides 24/7 uptime.

## What will not provide a permanent host

| Service | Why it is not a 24/7 solution for this app |
|---|---|
| GitHub Actions | Jobs are temporary CI runs and end when the workflow finishes. Use it for syntax checks, not a permanent bot. |
| GitHub Codespaces | Free compute is limited and development environments can stop; it is not a guaranteed always-on server. |
| Render free web services | Sleeping web services are not a suitable persistent Android emulator/Appium host. |
| Termux on the same Android phone | It can run Python processes, but it cannot straightforwardly control a separate full Rave Android UI through the current Appium setup without a compatible device/ADB or accessibility bridge. |

See the official [GitHub Actions billing documentation](https://docs.github.com/en/billing/concepts/product-billing/github-actions) and [Codespaces billing information](https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces).

## Known-working fallback (not cloud)

The most practical fully free route remains a Windows PC that stays powered on:

1. Install Node.js LTS, Android Studio, Android SDK Platform-Tools, and Android Emulator.
2. Create and boot an Android virtual device; install Rave from a trusted source and sign in manually.
3. Install Python 3.10+ and run `rave_bot/setup_windows.ps1`.
4. Copy `rave_bot/.env.example` to `rave_bot/.env` and fill in the Telegram token and numeric Telegram user ID privately.
5. Start with `rave_bot/start_windows.ps1 -AvdName "YOUR_AVD_NAME"`.
6. Use `/screenshot` and `/dumpui` in Telegram, then configure the chat selectors based on the actual UI.
7. Keep the PC awake and connected. Never commit `.env`.

## Security and readiness

- Never commit or send your Telegram bot token, Rave password, or private login data.
- Keep Appium bound to localhost; do not expose port 4723 to the public internet.
- The project is experimental. The Rave login, deep links, and chat selectors still require real-device/emulator testing.
- A successful GitHub Actions syntax check does not prove that Rave automation works.
