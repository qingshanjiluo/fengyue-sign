import requests
import os
import sys

# 从环境变量读取凭据
EMAIL = os.getenv('CHECKIN_EMAIL')
PASSWORD = os.getenv('CHECKIN_PASSWORD')

if not EMAIL or not PASSWORD:
    print('错误：未设置 CHECKIN_EMAIL 或 CHECKIN_PASSWORD 环境变量')
    sys.exit(1)

session = requests.Session()
BASE_URL = 'https://aisearches.xyz'

# 模拟登录
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
}

try:
    resp = session.post(
        f'{BASE_URL}/console/api/login',
        json=login_payload,
        headers=login_headers,
        timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    print('登录成功')
    # 提取 token（根据返回结构自行调整，这里假定在 data['token'] 中）
    token = data.get('token') or data.get('access_token')
    if not token:
        print('登录响应中未找到 token，请检查返回数据结构')
        sys.exit(1)
except Exception as e:
    print(f'登录失败：{e}')
    sys.exit(1)

# 携带 token 执行签到（请根据实际抓包修正接口）
auth_headers = {
    'User-Agent': login_headers['User-Agent'],
    'Authorization': f'Bearer {token}',
    'Referer': f'{BASE_URL}/zh/checkin',
}

# 推测的签到接口（常见为 GET 或 POST，请替换为实际 API）
checkin_url = f'{BASE_URL}/console/api/checkin'  # 请替换为实际地址
try:
    # 若实际为 POST，请改用 resp = session.post(checkin_url, json={...}, headers=auth_headers)
    resp = session.get(checkin_url, headers=auth_headers, timeout=30)
    if resp.status_code == 200:
        print('签到请求成功')
        print('响应内容：', resp.text)
    else:
        print(f'签到请求失败，状态码：{resp.status_code}')
        print(resp.text)
except Exception as e:
    print(f'签到请求异常：{e}')
