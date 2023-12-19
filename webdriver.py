from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

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
        wait_for_visibility("//td")
    else:
        option = wait_for_clickable(f"//label[text()='{option_text}']")
    option.click()

# 웹드라이버 객체 생성
driver = webdriver.Chrome()

# 웹사이트 접속
driver.get("https://geonode.com/free-proxy-list")

# 필터 설정
select_option('Country', 'South Korea', search=True)
print("Country: South Korea")
time.sleep(3)
select_option('Anonymity', 'Elite (HIA)')
print("Anonymity: Elite (HIA)")
time.sleep(3)
select_option('Proxy protocol', 'SOCKS4')
print("Proxy protocol: SOCKS4")

# 테이블의 모든 행이 로드될 때까지 기다립니다.
rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tr")))

# IP와 포트를 저장할 리스트를 생성합니다.
ip_port_list = []

# 테이블의 모든 행에서 열을 찾습니다.
for row in rows:
    # IP 주소와 포트가 로드될 때까지 기다립니다.
    ip_address = WebDriverWait(row, 10).until(EC.presence_of_element_located((By.XPATH, ".//td[1]"))).text
    port = WebDriverWait(row, 10).until(EC.presence_of_element_located((By.XPATH, ".//td[2]"))).text

    # IP와 포트를 묶어서 리스트에 추가합니다.
    ip_port = {"ip": ip_address, "port": port}
    ip_port_list.append(ip_port)

    # 결과를 바로 출력합니다.
    print(ip_address, port)
    print(f"{ip_port['ip']}:{ip_port['port']}")
    print(ip_port)

# 웹드라이버 종료
driver.quit()