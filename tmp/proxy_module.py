import requests
import random

# 무료 프록시 서버 목록
proxies_list = [
    'http://proxy1:port',
    'http://proxy2:port',
    # 추가 프록시 주소
]

def get_random_proxy():
    return {
        'http': random.choice(proxies_list),
        'https': random.choice(proxies_list)
    }

while True:
    proxy = get_random_proxy()
    try:
        # 프록시를 사용하여 요청
        response = requests.get('http://example.com', proxies=proxy, timeout=5)
        print(response.status_code)
    except requests.RequestException as e:
        print(f"Error with proxy {proxy}: {e}")
