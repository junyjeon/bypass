import requests
import random
from lxml.html import fromstring
import socks
import socket
import time

# def get_proxies():
#     url = 'https://free-proxy-list.net/'
#     response = requests.get(url)
#     parser = fromstring(response.text)
#     proxies = set()
#     for i in parser.xpath('//tbody/tr')[:100]:
#         proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
#         proxies.add(proxy)
#     return proxies

def get_proxies():
    url = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&country=KR&protocols=socks4%2Csocks5&anonymityLevel=elite'
    response = requests.get(url)
    print(response)
    data = response.json()
    proxies = set()
    for proxy_data in data['data']:
        proxy = f"{proxy_data['ip']}:{proxy_data['port']}"
        proxies.add(proxy)
    return proxies

def get_current_ip(proxy=None):
    try:
        if proxy:
            response = requests.get('http://ip.42.pl/raw', proxies={"http": proxy, "https": proxy})
        else:
            response = requests.get('http://ip.42.pl/raw')
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Get current IP before changing proxy
print(f"Current IP before changing proxy: {get_current_ip()}")

def check_proxy(proxy):
    try:
        response = requests.get('http://ip.42.pl/raw', proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.ok:
            return True
        else:
            return False
    except:
        return False

# Get proxies
proxies = get_proxies()
print(proxies)

# Choose a different proxy
proxy = random.choice(list(proxies))

# Check if the proxy is working
while not check_proxy(proxy):
    proxy = random.choice(list(proxies))

# Start time
start_time = time.time()

# Set up PySocks with the new proxy
socks.set_default_proxy(socks.HTTP, proxy.split(':')[0], int(proxy.split(':')[1]))

# Get current IP after changing proxy
print(f"Current IP after changing proxy: {get_current_ip(proxy)}")

# End time
end_time = time.time()

# Calculate and print the time taken
print(f"Time taken to change IP: {end_time - start_time} seconds")

response = requests.get('https://www.naver.com', proxies={"http": proxy, "https": proxy})
print(response.status_code)
# socks.set_default_proxy(socks.SOCKS5, "localhost", 1080)
# socket.socket = socks.socksocket

# print(requests.get('http://icanhazip.com', proxies={"http": "http://127.0.0.1", "https": "http://127.0.0.1"}).text)

#엘리트 프록시
#socks5