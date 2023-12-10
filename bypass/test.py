import time
import subprocess
import json
import asyncio
import aiohttp

def load_settings():
    with open('settings.json') as f:
        return json.load(f)

async def check_proxy_ip(session):
    """
    현재 프록시 IP 주소를 확인하고 반환합니다.
    IP 주소를 가져오는 데 실패하면 None을 반환합니다.
    """
    try:
        async with session.get('http://ip.42.pl/raw') as response:
            return await response.text()
    except Exception as e:
        print(f"Error occurred while getting IP: {e}")
        return None

def switch_proxy_server(current_proxy_index, config_files):
    """
    현재 프록시 서버를 중지하고 다음 프록시 서버를 시작합니다.
    current_proxy_index는 현재 사용 중인 프록시 서버의 인덱스입니다.
    """
    subprocess.run(["pkill", "sslocal"])
    config_file = config_files[current_proxy_index]
    subprocess.run(["sslocal", "-c", config_file])
    current_proxy_index = (current_proxy_index + 1) % len(config_files)
    return current_proxy_index

async def main_function():
    """
    주기적으로 IP 주소를 확인하고, IP 주소가 변경되지 않았다면 프록시 서버를 전환합니다.
    프록시 서버 전환 후에도 IP 주소가 변경되지 않는다면, 프록시 서버 전환을 계속 시도합니다.
    """
    settings = load_settings()
    config_files = settings['config_files']
    current_proxy_index = 0
    used_ips = {}

    async with aiohttp.ClientSession() as session:
        while True:
            original_ip = await check_proxy_ip(session)
            if original_ip is None:
                print("Failed to get original IP. Retrying...")
                time.sleep(settings['sleep_time'])
                continue

            time.sleep(settings['sleep_time'])

            new_ip = await check_proxy_ip(session)
            if new_ip is None:
                print("Failed to get new IP. Retrying...")
                time.sleep(settings['sleep_time'])
                continue

            while new_ip == original_ip or (new_ip in used_ips and used_ips[new_ip] > time.time()):
                try:
                    current_proxy_index = switch_proxy_server(current_proxy_index, config_files)
                    time.sleep(settings['sleep_time'])
                    new_ip = await check_proxy_ip(session)
                except Exception as e:
                    print(f"Error occurred while switching proxy server: {e}")
                    time.sleep(settings['sleep_time'])

            used_ips[new_ip] = time.time() + 30

loop = asyncio.get_event_loop()
loop.run_until_complete(main_function())