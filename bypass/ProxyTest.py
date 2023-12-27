import requests
import socks
import socket
from urllib.parse import urlparse
import time

# 프록시 URL 생성
proxy = "socks5://121.129.47.25:1080"

# 프록시 URL 파싱
parsed_proxy = urlparse(proxy)

# Shadowsocks-rust 프록시 설정
socks.set_default_proxy(socks.SOCKS5, parsed_proxy.hostname, parsed_proxy.port)
socket.socket = socks.socksocket

print(f"Proxy changed to: {parsed_proxy.hostname}:{parsed_proxy.port}")

# 요청 전의 시간을 측정합니다.
start_time = time.time()

# 프록시를 사용하여 요청 보내기
response = requests.get('https://ifconfig.me/ip', proxies={"http": proxy, "https": proxy})
print(f"Current IP: {response.text.strip()}")

# 요청 후의 시간을 측정합니다.
end_time = time.time()

# 요청 시간을 계산합니다.
request_time = end_time - start_time

print(f"Request time: {request_time} seconds")
print(f"Response status code: {response.status_code}")