import os
import sys
from playwright.sync_api import sync_playwright

EMAIL = os.getenv('CHECKIN_EMAIL', '').strip()
PASSWORD = os.getenv('CHECKIN_PASSWORD', '').strip()

if not EMAIL or not PASSWORD:
    print('❌ 环境变量 CHECKIN_EMAIL 或 CHECKIN_PASSWORD 未设置')
    sys.exit(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
    )
    page = context.new_page()

    # ---------- 登录 ----------
    page.goto('https://aisearches.xyz/zh/signin')
    page.wait_for_selector('input[name="email"]', timeout=15000)
    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"]')          # 或 'button:has-text("登录")'
    
    # 等待登录成功（跳转到 explore 页面）
    try:
        page.wait_for_url('**/explore/**', timeout=15000)
        print('✅ 登录成功')
    except:
        print('⚠️ 登录可能失败，检查页面截图 login_error.png')
        page.screenshot(path='login_error.png')
        sys.exit(1)

    # ---------- 签到 ----------
    page.goto('https://aisearches.xyz/zh/checkin')
    page.wait_for_timeout(3000)      # 等待页面渲染

    # 尝试点击签到按钮（根据常见文案）
    clicked = False
    for btn_text in ['签到', '立即签到', '每日签到']:
        try:
            page.click(f'button:has-text("{btn_text}")', timeout=5000)
            print(f'✅ 点击了“{btn_text}”按钮')
            clicked = True
            break
        except:
            continue
    
    if not clicked:
        # 可能按钮是其他文案，或者已经签过到，截图保存现场
        print('ℹ️ 未找到签到按钮（可能已签到或按钮文案不同），保存截图')
    
    # 等待结果并截图
    page.wait_for_timeout(3000)
    page.screenshot(path='checkin_result.png')
    print('🎉 签到流程结束，结果截图已保存')
    browser.close()
