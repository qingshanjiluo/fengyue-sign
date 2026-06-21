import requests
import os
import sys

EMAIL = os.getenv('CHECKIN_EMAIL')
PASSWORD = os.getenv('CHECKIN_PASSWORD')

if not EMAIL or not PASSWORD:
    print('错误：未设置 CHECKIN_EMAIL 或 CHECKIN_PASSWORD')
    sys.exit(1)

session = requests.Session()
BASE_URL = 'https://aisearches.xyz'

# 模拟浏览器预请求首页以获取 cookie（有时必需）
try:
    session.get(f'{BASE_URL}/zh/signin', timeout=30)
except:
    pass

login_payload = {
    'email': EMAIL,
    'password': PASSWORD,
    'remember_me': True,
    'interface_language': 'zh-Hans'
}

login_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': BASE_URL,
    'Referer': f'{BASE_URL}/zh/signin',
    'x-timezone': 'Asia/Shanghai',
    'x-language': 'zh-Hans',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
}

try:
    resp = session.post(
        f'{BASE_URL}/console/api/login',
        json=login_payload,
        headers=login_headers,
        timeout=30
    )
    print('登录状态码:', resp.status_code)
    print('登录响应:', resp.text[:500])  # 只打印前500字符防止过长
    resp.raise_for_status()
    data = resp.json()
    print('登录成功')
    token = data.get('token') or data.get('access_token')
    if not token:
        print('响应中未找到 token，完整响应：')
        print(resp.text)
        sys.exit(1)
except Exception as e:
    print(f'登录失败：{e}')
    sys.exit(1)
