import asyncio
import json
import re
import time

from playwright.async_api import TimeoutError as PlaywrightTimeoutError


async def open_jio_checkout(page, config, hook, update_state, log, check_stop):
    await page.context.add_init_script(hook + "\nwindow.__setDirectTest(" + json.dumps(config) + ");")
    await page.goto("https://one.google.com/upsell?hl=en-US&gl=US", wait_until="domcontentloaded", timeout=40000)
    await page.evaluate("window.__setDirectTest(" + json.dumps(config) + ")")
    log("Jio plan detected: selecting AI Plus 2 TB as the offer trigger; Jio will be replaced if checkout succeeds.")
    update_state(status="running", current_step=2, step_message="Opening Jio replacement checkout")
    title = page.get_by_text(re.compile(r'^Google AI Plus\s*\(2\s*TB\)$', re.I), exact=True).first
    await title.scroll_into_view_if_needed(timeout=30000)
    button = title.locator('xpath=following::*[self::button or @role="button"][normalize-space(.)="Get started"][1]')
    await button.click(timeout=30000)
    await page.get_by_role('button', name='Continue', exact=True).click(timeout=30000)
    await page.get_by_role('button', name='Yes, continue', exact=True).click(timeout=30000)
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        check_stop()
        if page.is_closed():
            raise RuntimeError('Browser closed before checkout')
        for frame in page.frames:
            if 'eacquire' not in frame.url:
                continue
            try:
                text = await frame.locator('body').inner_text(timeout=2000)
                subscribe = frame.get_by_role('button', name='Subscribe', exact=True)
                if await subscribe.count() == 0 or not await subscribe.first.is_visible():
                    continue
                normalized = ' '.join(text.split())
                today = re.search(r'\bToday\s+(?:US\$|\$)0[.,]00(?=\s|$)', normalized, re.I)
                product = re.search(r'Google AI Pro\s*\(5\s*TB\)', normalized, re.I)
                if not today or not product:
                    raise RuntimeError('Checkout blocked: expected Google AI Pro (5 TB) and Today US$0.00 were not both confirmed')
                log('Checkout confirms Google AI Pro 5 TB and Today $0.00; clicking Subscribe once. Future recurring charges may apply.')
                update_state(status='running', current_step=2, step_message='Submitting Jio replacement; do not retry until order status is checked')
                try:
                    await subscribe.first.click(timeout=5000)
                except PlaywrightTimeoutError as exc:
                    raise RuntimeError('Subscribe outcome unknown. Check Google Play orders before retrying.') from exc
                log('Subscribe submitted once. Waiting for explicit membership confirmation; do not retry.')
                update_state(status='running', current_step=2, step_message='Waiting for membership confirmation; do not retry')
                deadline = time.monotonic() + 120
                while time.monotonic() < deadline:
                    check_stop()
                    if page.is_closed():
                        raise RuntimeError('Browser closed; subscription outcome unconfirmed. Check Google Play before retrying.')
                    for current in page.context.pages:
                        for current_frame in current.frames:
                            try:
                                body = await current_frame.locator('body').inner_text(timeout=1000)
                                if 'Get Google Play Points from purchases like this' in body:
                                    dismiss = current_frame.get_by_role('button', name='Not now', exact=True)
                                    if await dismiss.count() and await dismiss.first.is_visible():
                                        await dismiss.first.click(timeout=3000)
                                if re.search(r'Your new membership is ready', body, re.I):
                                    done = current_frame.get_by_role('button', name='Done', exact=True)
                                    if await done.count() and await done.first.is_visible():
                                        await done.first.click(timeout=3000)
                                    log('Google One confirmed the new membership; proceeding to tier 2.')
                                    return True
                            except PlaywrightTimeoutError:
                                continue
                    await asyncio.sleep(1)
                raise RuntimeError('Subscription outcome unconfirmed. Check Google Play orders and subscriptions before retrying.')
            except PlaywrightTimeoutError:
                continue
        await asyncio.sleep(1)
    raise TimeoutError('Google Play checkout not found; no subscription submitted')
