import requests
import time

# 프록시 URL 생성
proxy = "socks4://localhost:1080"  # Shadowsocks-rust 클라이언트가 실행 중인 주소

# 요청 전의 시간을 측정합니다.
start_time = time.time()

# 프록시를 사용하여 요청 보내기
response = requests.get('https://www.where42.kr/Login', proxies={"http": proxy, "https": proxy})
print(f"Response status code: {response.status_code}")

# 요청 후의 시간을 측정합니다.
end_time = time.time()

# 요청 시간을 계산합니다.
request_time = end_time - start_time

print(f"Request time: {request_time} seconds")