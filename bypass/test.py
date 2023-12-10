import time
import subprocess
import json
import asyncio
import aiohttp
import logging
import random
from typing import Dict, Any

def load_settings(file_path: str) -> Dict[str, Any]:
    with open(file_path) as f:
        return json.load(f)

settings = load_settings('settings.json')

async def check_proxy_ip(session: aiohttp.ClientSession) -> str:
    try:
        async with session.get('http://ip.42.pl/raw') as response:
            return await response.text()
    except aiohttp.ClientError as e:
        logging.error(f"Network error occurred while getting IP: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error occurred while getting IP: {e}")
        return None

def switch_proxy_server(config_files: list) -> str:
    subprocess.run(["pkill", "sslocal"])
    config_file = random.choice(config_files)
    subprocess.run(["sslocal", "-c", config_file])
    return config_file

async def sleep_with_message(sleep_time: int, message: str) -> None:
    logging.info(message)
    await asyncio.sleep(sleep_time)

async def handle_ip(session: aiohttp.ClientSession, config_files: list, used_ips: set) -> str:
    while True:
        ip = await check_proxy_ip(session)
        if ip is not None and ip not in used_ips:
            break
        config_file = switch_proxy_server(config_files)
        await sleep_with_message(settings['sleep_time'], f"Switched to proxy server {config_file}. Waiting...")
    used_ips.add(ip)
    asyncio.get_event_loop().call_later(settings['expiry_time'], used_ips.remove, ip)
    return ip

async def main_function(loop: asyncio.AbstractEventLoop) -> None:
    config_files = settings['config_files']
    used_ips = set()

    async with aiohttp.ClientSession() as session:
        while True:
            ip = await handle_ip(session, config_files, used_ips)
            if ip is not None:
                break
            await asyncio.sleep(settings['sleep_time'])

loop = asyncio.get_event_loop()
loop.run_until_complete(main_function(loop))