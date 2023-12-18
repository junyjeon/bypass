import requests
import socks
import socket
from urllib.parse import urlparse

# 프록시 URL 생성
proxy = "socks5://221.167.75.138:5156"

# 프록시 URL 파싱
parsed_proxy = urlparse(proxy)

# Shadowsocks-rust 프록시 설정
socks.set_default_proxy(socks.SOCKS4, parsed_proxy.hostname, parsed_proxy.port)
socket.socket = socks.socksocket

# 프록시를 사용하여 요청 보내기
response = requests.get('http://ip.42.pl/raw', proxies={"http": proxy, "https": proxy})
print(response.status_code)