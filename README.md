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

========================================================================
  Google AI Pro (5 TB) 零成本两年 (US$0.00 -> 24个月) 全自动控制台
========================================================================

【一、运行环境要求】
1. Windows 10 / 11 系统
2. 已安装 Google Chrome 浏览器（默认路径即可）
3. 已安装 Python 3.10 或更高版本（安装时勾选 Add Python to PATH）
4. 网络环境：本机开启美区（US）代理，或在控制台左侧填写代理模板

【二、快速启动步骤】
1. 首次使用请双击运行：【1_首次运行_安装依赖并启动.bat】
2. 之后日常使用直接双击：【2_启动控制台.bat】
3. 浏览器会自动打开控制台页面：http://127.0.0.1:8765

【三、自定义填写支付卡 & 跑号说明】
1. 填写支付卡（必填）：
   - 在网页左侧【全局配置与内联免税绑卡】区域，填入你自己的 Visa 或 Mastercard 外币卡：
     * 卡号（16位数字）
     * 有效期（月 / 年，如 08 / 29）
     * 安全码（3位 CVC）
     * 持卡人英文姓名
     * 免税邮编默认已填好 97201（美国俄勒冈免税州），无需修改
   - 填写后点击【💾 保存配置】。
   - 注：脚本内置严格 0 元消费保护，仅在结账弹窗确认为 US$0.00 时才会点击订阅，全程 0 扣费。

2. 批量导入 Google 账号：
   - 在网页右侧【批量放号导入区】粘贴账号（每行一个），支持以下任意格式：
     * 邮箱----密码----辅助邮箱
     * 邮箱----密码
   - 点击【➕ 一键导入账号列表】。

3. 开始全自动执行：
   - 点击单个账号右侧的【▶ 执行】或顶部的【▶ 批量全自动执行】。
   - 脚本会自动完成：
     Step 1: 自动填写登录账号密码，Google 验证由用户在浏览器中手动完成
     Step 2: 内联免税绑卡 + 首层 12 个月免费包 (US$0.00)
     Step 3: 叠加二层 6 个月免费包 (US$0.00 -> 18个月)
     Step 4: 叠加三层 6 个月免费包 (US$0.00 -> 24个月封顶)
     Step 5: 自动前往 Google Play 取消自动续订，锁死 2 年到期权益并截图验真


# 卡网：https://faka.cdkey.si
# 博客：https://blog.caowo.de
# TG群：@Hello_Florence
