from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service

# 직접 다운로드한 ChromeDriver의 경로를 지정합니다.
chrome_driver_path = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

# webdriver.Chrome()에 ChromeDriver의 경로를 전달합니다.
driver = webdriver.Chrome(service=Service(chrome_driver_path))

# 웹사이트 접속
driver.get("https://geonode.com/free-proxy-list")

# 필터 설정
country_select = Select(driver.find_element_by_id("country의 ID"))
country_select.select_by_visible_text("South Korea")

anonymity_select = Select(driver.find_element_by_id("anonymity의 ID"))
anonymity_select.select_by_visible_text("Elite (HIA)")

protocol_select = Select(driver.find_element_by_id("protocol의 ID"))
protocol_select.select_by_visible_text("SOCKS4")
protocol_select.select_by_visible_text("SOCKS5")

# 필터 적용 버튼 클릭
apply_button = driver.find_element_by_id("apply button의 ID")
apply_button.click()

# 결과 추출
table = driver.find_element_by_css_selector("table의 CSS 선택자")
rows = table.find_elements_by_tag_name("tr")

for row in rows:
    columns = row.find_elements_by_tag_name("td")
    ip_address = columns[0].text
    port = columns[1].text
    protocol = columns[3].text

    print(ip_address, port, protocol)

# 웹드라이버 종료
driver.quit()