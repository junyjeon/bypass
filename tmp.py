import subprocess
import time

# 프록시 서버 설정 파일의 경로를 저장하는 리스트
config_files = [f"conf/config{i}.json" for i in range(1, 31)]

# 현재 사용 중인 프록시 서버의 인덱스
current_proxy_index = 0

def check_proxy_ip():
    # 현재 프록시 IP 주소 확인 로직
    return current_ip

def switch_proxy_server():
    # 프록시 서버 전환 로직
    pass

def main_function():
    original_ip = check_proxy_ip()
    # 메인 함수 로직
    new_ip = check_proxy_ip()
    if new_ip == original_ip:
        switch_proxy_server()
        main_function() # 함수 재실행

main_function()

def use_next_proxy():
    global current_proxy_index

    # 현재 프록시 서버를 중지
    subprocess.run(["pkill", "sslocal"])

    # 다음 프록시 서버를 시작
    config_file = config_files[current_proxy_index]
    subprocess.run(["sslocal", "-c", config_file])

    # 다음 프록시 서버를 가리키도록 인덱스를 업데이트
    current_proxy_index = (current_proxy_index + 1) % len(config_files)

# 테스트를 위한 메인 함수
def main():
    while True:
        use_next_proxy()
        time.sleep(30)

if __name__ == "__main__":
    main()