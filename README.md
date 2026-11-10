## Linux / Brave

Requires Python 3.10+, a graphical desktop session and Chrome, Chromium or Brave. Windows remains supported through the included batch files.

```bash
uv venv
uv pip install -r requirements.txt
BROWSER_PATH=/usr/bin/brave .venv/bin/python app.py
```

For fish shell, use `env BROWSER_PATH=/usr/bin/brave .venv/bin/python app.py`. Replace the path with the executable reported by `which brave` or `which brave-browser`. `BROWSER_PATH` is optional: without it the app searches for Chrome, Chromium and Brave. Open http://127.0.0.1:8765 in a browser. The automated browser is visible, not headless.

Browser profiles and screenshots are saved locally in `profiles/` and `screenshots/`; account and card configuration is stored unencrypted in `config.json`. Protect these files. Verify prices and eligibility before subscribing; a free offer is not guaranteed.

Google verification is manual: import `email----password` (optionally append `----recovery-email`), then complete any Google challenge in the opened browser. The automation waits up to 10 minutes; stop the task to cancel. No authenticator secret is required. Previously saved `totp_secret` values are not used or displayed, but remain in existing `config.json` files until you remove them yourself.

Google One and Google Play URLs request US English (`hl=en-US`, `gl=US`). Google may still use account, payment-profile, or other regional settings; these URL parameters do not change eligibility or billing country.

If a Jio-managed plan is detected, the app opens Google One upsell, selects Google AI Plus 2 TB as the trigger and injects the existing first-tier offer. It clicks Subscribe once only when checkout shows Google AI Pro (5 TB) and Today US$0.00; otherwise it stops. This can replace the Jio benefit and start recurring charges after the trial. After explicit Google One membership confirmation, it continues to tier 2. If confirmation is absent, check Google Play subscriptions and orders before any retry. Starting from tier 2 skips the Jio replacement flow.

If settings shows only Google One settings and email preferences without a membership status, the pipeline proceeds to the standard plans checkout after the status wait. This page layout alone does not prove offer eligibility.

Tier 2 (Step 3) submits once even if checkout does not show a zero-cost trial. Google can impose immediate or recurring charges; check the displayed terms and your subscriptions. An ambiguous result is not retried automatically.
