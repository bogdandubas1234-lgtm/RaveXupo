# Free hosting: realistic options for RaveXupo

## Short answer

There is no dependable free cloud host that we can honestly promise will keep **an authenticated Rave Android app + Android emulator + Appium + Telegram bot** running 24/7.

### Options

| Option | Cost | Works 24/7? | Fits this project? |
|---|---:|---|---|
| GitHub Actions | $0 within applicable quotas | No; each job ends | Good for tests, not permanent hosting |
| Render free web service | $0 within quota | No; sleeps after 15 minutes without inbound traffic | Not suitable for an emulator/Appium process |
| Free cloud VM | Usually advertised as $0 within limits | Potentially, subject to provider and resource limits | Not dependable for this workload; virtualization, RAM and CPU are the blockers |
| Your own Windows PC + Android emulator | $0 additional hosting fee | Only while the PC is on and awake | Most practical fully free option |

GitHub Actions supports emulator testing in some runner configurations, but those runners are temporary CI machines; the emulator is shut down when the job finishes. Do not add a keep-alive loop or repeated workflows to try to turn CI into a permanent server.

## Recommended no-cost route

1. Use the Windows setup scripts in `rave_bot/`.
2. Install Android Studio and create an Android virtual device.
3. Install Rave and sign in manually in that emulator.
4. Configure the Telegram bot token and your numeric Telegram user ID in a local `.env` file only.
5. Run `start_windows.ps1`, then use `/screenshot` and `/dumpui` to inspect the actual app UI.
6. Configure chat selectors only after they are discovered from your installed Rave version.
7. Disable sleep while plugged in; keep the PC running.

## If the PC must be off

Then a cloud machine is required. The truly free options available today are not a dependable fit for a persistent Android emulator. A paid x86-64 VPS with enough RAM and nested virtualization may work, but Rave login, emulator compatibility and chat selectors still need to be tested before paying for anything.
