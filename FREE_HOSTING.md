# Free hosting for RaveXupo (phone-only setup)

## Honest answer first

RaveXupo currently automates the **Rave Android app** through Appium. A working deployment therefore needs all of these at once:

- a persistent Android device or emulator;
- Rave installed and manually signed in;
- Appium and the Python Telegram controller;
- stable access to the device UI, plus configured selectors for the current Rave version.

A free Linux server is **not automatically an Android emulator host**. No cloud option has been verified end-to-end for this repository, so this guide does not promise free 24/7 operation.

## Cloud option to investigate: Oracle Cloud Always Free

Oracle Cloud Infrastructure (OCI) is the most plausible free VM experiment because its Always Free resources can include small AMD VMs and an Ampere A1 ARM VM. Check the current official limits before creating anything:

- [Oracle Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)
- [Oracle Free Tier FAQ](https://www.oracle.com/cloud/free/faq/)

Important limitations:

- OCI signup may require a valid payment card for verification; an authorization hold may appear.
- VM capacity is not guaranteed. An "out of host capacity" error can mean you must wait or try another availability domain.
- The Always Free Ampere A1 allowance is ARM-based. Android Emulator hardware acceleration and guest image compatibility are the key unknowns for this project. Do not assume that an ARM cloud VM can run the required Android emulator reliably.
- The tiny AMD Always Free VM is not a realistic target for a full Android emulator + Appium + Rave workload.
- Free-tier terms and quotas can change. Confirm that the instance is explicitly marked Always Free before creating it, and do not enable paid resources.

### Phone-only preflight checklist

You can do these steps from your phone browser; no computer is needed to create the cloud account:

1. Open the official OCI Free Tier page and review the card-verification and regional availability requirements.
2. Create one account only, using accurate details. Do not create duplicate accounts to get around capacity or eligibility limits.
3. In the OCI Console, check the available Always Free compute shapes in your home region.
4. **Stop before deploying RaveXupo** if the only available free instance cannot support a compatible Android emulator. Do not add payment details to upgrade or create paid resources just to test this.
5. If you do obtain a suitable VM, first test Android Emulator, Appium, and a manually authenticated Rave installation separately. Only then configure this bot. This has not been tested for this repository.

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
