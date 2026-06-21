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
    page.goto('https://aisearches.xyz/zh/signin', wait_until='networkidle')

    # 等待邮箱输入框出现（通过占位符文字）
    email_input = page.get_by_placeholder('邮箱')
    # 如果中文占位符不生效，尝试英文
    if not email_input.is_visible():
        email_input = page.get_by_placeholder('Email')
    email_input.wait_for(timeout=15000)
    email_input.fill(EMAIL)

    # 密码框
    password_input = page.get_by_placeholder('密码')
    if not password_input.is_visible():
        password_input = page.get_by_placeholder('Password')
    password_input.fill(PASSWORD)

    # 点击登录按钮
    login_button = page.get_by_role('button', name='登录')
    if not login_button.is_visible():
        login_button = page.get_by_role('button', name='Sign in')
    login_button.click()

    # 等待登录跳转或出现“签到”链接（说明已登录）
    try:
        page.wait_for_url('**/explore/**', timeout=15000)
        print('✅ 登录成功')
    except:
        # 备用：等待“签到”或“退出”按钮出现
        try:
            page.wait_for_selector('text=签到', timeout=10000)
            print('✅ 登录成功（通过文字判断）')
        except:
            print('❌ 登录可能失败，保存截图')
            page.screenshot(path='login_error.png')
            sys.exit(1)

    # ---------- 签到 ----------
    page.goto('https://aisearches.xyz/zh/checkin', wait_until='networkidle')
    page.wait_for_timeout(3000)

    # 尝试点击签到按钮（多种文案）
    checkin_button = page.get_by_role('button', name='签到')
    if not checkin_button.is_visible():
        checkin_button = page.get_by_role('button', name='立即签到')
    if not checkin_button.is_visible():
        checkin_button = page.get_by_role('button', name='每日签到')

    if checkin_button.is_visible():
        checkin_button.click()
        print('✅ 已点击签到按钮')
    else:
        print('ℹ️ 未找到签到按钮（可能已签到）')

    page.wait_for_timeout(3000)
    page.screenshot(path='checkin_result.png')
    print('🎉 流程结束，截图已保存')
    browser.close()
