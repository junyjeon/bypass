from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import itertools
import json
import requests
import subprocess
import time
import socks
import socket
from selenium.webdriver.chrome.options import Options
import concurrent.futures

def get_proxies():
    # 사용자 에이전트 문자열을 설정합니다.
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

    # 옵션 객체를 생성하고 사용자 에이전트를 설정합니다.
    options = Options()
    options.add_argument(f'user-agent={user_agent}')

    # 웹드라이버 객체 생성
    driver = webdriver.Chrome()

    def wait_for_element(xpath, timeout=10):
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def wait_for_clickable(xpath, timeout=10):
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def wait_for_visibility(xpath, timeout=10):
        return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def select_option(label_text, option_text, search=False):
        if label_text == 'Country':
            button = wait_for_element(f"//label[contains(text(), '{label_text}')]/following-sibling::div//button")
        else:
            button = wait_for_element(f"//label[contains(text(), '{label_text}')]/ancestor::div/following-sibling::div//button")
        button.click()

        if search:
            search_field = wait_for_element("//input[@placeholder='Search']")
            search_field.send_keys("Kore")

        if label_text == 'Country':
            option =wait_for_clickable(f"//li//span[contains(text(), '{option_text}')]")
        else:
            option = wait_for_clickable(f"//label[text()='{option_text}']")
        option.click()
        time.sleep(2)

    # 웹사이트 접속
    driver.get("https://geonode.com/free-proxy-list")

    # 필터 설정
    time.sleep(1)
    select_option('Country', 'South Korea', search=True)
    print("Country: South Korea")
    select_option('Anonymity', 'Elite (HIA)')
    print("Anonymity: Elite (HIA)")
    select_option('Proxy protocol', 'SOCKS4')
    print("Proxy protocol: SOCKS4")
    time.sleep(1)

    rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tr")))
    proxies = []

    for row in rows[1:]:
        try:
            ip_address = WebDriverWait(row, 10).until(EC.presence_of_element_located((By.XPATH, ".//td[1]/span"))).text
            port = WebDriverWait(row, 10).until(EC.presence_of_element_located((By.XPATH, ".//td[2]/span"))).text

            ip_port = {"ip": ip_address, "port": port}
            proxies.append(ip_port)

            print(ip_port)
        except Exception as e:
            print(f"Error: {e}")
    # 웹드라이버 종료
    driver.quit()
    return proxies

def change_shadowsocks_config(ip, port):
    print(f"Changing proxy to {ip}:{port}")
    with open('shadowsocks.json', 'r') as f:
        config = json.load(f)

    config['server'] = ip
    config['server_port'] = port

    with open('shadowsocks.json', 'w') as f:
        json.dump(config, f, indent=4)
    print("Done")

def ping(ip):
    # 'ping' 명령을 사용하여 프록시 서버의 응답 시간을 측정합니다.
    # 이 코드는 Linux와 macOS에서 작동합니다. Windows에서는 수정이 필요할 수 있습니다.
    try:
        output = subprocess.check_output("ping -c 1 " + ip, shell=True)
        ms_index = output.find(b"ms")
        time_start_index = output.rfind(b"=", 0, ms_index)
        time_end_index = output.find(b" ", time_start_index)
        time = float(output[time_start_index+1:time_end_index])
        return time
    except Exception:
        return 99999

def sort_proxies_by_ping(proxies):
    # 각 프록시의 응답 시간을 측정하고, 이를 기준으로 프록시 리스트를 정렬합니다.
    for proxy in proxies:
        proxy['ping'] = ping(proxy['ip'])
    proxies.sort(key=lambda x: x['ping'])
    return proxies

def check_proxy(proxy, timeout=60):
    # 프록시 서버에 HTTP 요청을 보내고 응답을 확인합니다.
    try:
        print(f"Checking proxy {proxy}")
        proxies = {
            'http': f'socks4://{proxy["ip"]}:{proxy["port"]}',
            'https': f'socks4://{proxy["ip"]}:{proxy["port"]}',
        }
        response = requests.get('https://ifconfig.me/ip', proxies=proxies, timeout=timeout)
        print(f"Proxy {proxy} is working")
        print(f"Status code: {response.status_code}")
        return response.status_code == 200
    except Exception:
        return False

def filter_working_proxies(proxies, max_workers=5):
    # 작동하는 프록시만 남깁니다.
    print(f"Total proxies: {len(proxies)}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        print(f"Max workers: {max_workers}")
        future_to_proxy = {executor.submit(check_proxy, f"{proxy['ip']}:{proxy['port']}"): proxy for proxy in proxies}
        print(f"Total futures: {len(future_to_proxy)}")
        return [future_to_proxy[future] for future in concurrent.futures.as_completed(future_to_proxy) if future.result()]

# 프록시 리스트를 가져옵니다.
proxies = get_proxies()
print(proxies)

# 프록시가 작동하는지 확인합니다.
for proxy in proxies:
    print(f'{proxy}: {check_proxy(proxy["ip"] + ":" + proxy["port"])}')

# 작동하는 프록시만 남깁니다.
print("filter_working_proxies")
proxies = filter_working_proxies(proxies)
print("filter_working_proxies")
print(proxies)

# 응답 시간이 빠른 순서로 프록시 리스트를 정렬합니다.
proxies = sort_proxies_by_ping(proxies)

# 프록시 리스트를 순환하는 이터레이터
proxy_iterator = itertools.cycle(proxies)

def change_proxy():
    global proxy_iterator
    print("Changing proxy")
    print(proxies)
    proxy = next(proxy_iterator)  # 다음 프록시를 가져옵니다.
    socks.set_default_proxy(socks.SOCKS4, proxy['ip'], int(proxy['port']))
    socket.socket = socks.socksocket
    print(f"Proxy changed to: {proxy['ip']}:{proxy['port']}")

def get_current_ip(proxy):
    # 외부 서비스를 사용하여 현재 IP 주소를 가져옵니다.
    response = requests.get('https://ifconfig.me/ip', proxies={'http': proxy, 'https': proxy})
    print(f"Current IP: {response.text.strip()}")
    return response.text.strip()

def get_original_ip():
    # 외부 서비스를 사용하여 현재 IP 주소를 가져옵니다.
    response = requests.get('https://ifconfig.me/ip')
    print(f"Original IP: {response.text.strip()}")
    return response.text.strip()

def test_change_proxy():
    # 프록시를 변경하고, IP 주소가 변경되었는지 확인합니다.
    print(f"Original IP: {get_original_ip()}")
    change_proxy()
    proxy = next(proxy_iterator)
    proxy_string = f"http://{proxy['ip']}:{proxy['port']}"
    print(f"New IP: {get_current_ip(proxy_string)}")

test_change_proxy()

# def reset_proxy():
#     with open('shadowsocks.json', 'r') as f:
#         config = json.load(f)

#     config['server'] = ""
#     config['server_port'] = ""

#     with open('shadowsocks.json', 'w') as f:
#         json.dump(config, f, indent=4)\
