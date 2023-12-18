import requests
import socks
import socket
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# 웹사이트 주소
url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&country=KR&protocols=socks4%2Csocks5&anonymityLevel=elite"

# 프록시 정보를 저장할 리스트
proxies = []

# 웹사이트에서 프록시 정보 가져오기
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

for row in soup.find_all('tr'):
    columns = row.find_all('td')
    ip_address = columns[0].get_text(strip=True)
    port = columns[1].get_text(strip=True)
    protocol = columns[3].get_text(strip=True).lower()  # socks4 또는 socks5

    # 프록시 정보를 리스트에 추가
    proxies.append((ip_address, port, protocol))

# 사용한 프록시를 저장할 리스트
used_proxies = []

for proxy in proxies:
    ip_address, port, protocol = proxy

    # 프록시 설정
    if protocol == 'socks4':
        socks_type = socks.SOCKS4
    elif protocol == 'socks5':
        socks_type = socks.SOCKS5
    else:
        continue  # socks4 또는 socks5가 아닌 경우 건너뛰기

    socks.set_default_proxy(socks_type, ip_address, int(port))
    socket.socket = socks.socksocket

    # 요청 전 시간 측정
    start_time = time.time()

    try:
        # 프록시를 사용하여 요청 보내기
        response = requests.get('http://ip.42.pl/raw', timeout=20)
        print("Status code:", response.status_code)

        # 요청 후 시간 측정
        end_time = time.time()

        # 요청에 걸린 시간 계산
        elapsed_time = end_time - start_time
        print("Elapsed time:", elapsed_time, "seconds")

        # 사용한 프록시를 리스트에 추가
        used_proxies.append(proxy)

        # 20초 동안 대기
        time.sleep(20)

    except requests.exceptions.RequestException:
        print("Request failed. Trying next proxy.")
        continue