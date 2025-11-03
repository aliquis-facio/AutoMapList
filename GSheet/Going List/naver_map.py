from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import List, Dict, Tuple
from webdriver_manager.chrome import ChromeDriverManager

# 3. 검색어 입력 및 검색
# search_keyword = input("장소: ")  # 원하는 검색어로 변경
search_keyword = "몽크투바흐"

# 1. Selenium WebDriver 설정
# driver's options
driver_options = Options()
driver_options.add_experimental_option(
    "excludeSwitches", ["enable-logging"])
driver_options.add_argument("headless")
wait_time: int = 5  # sec

# initialize the lastest driver
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=driver_options)
driver.implicitly_wait(wait_time)

# 2. 네이버 지도 페이지로 이동
driver.get('https://map.naver.com/')
driver.implicitly_wait(wait_time)

search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")  # 검색창 요소 선택
search_box.send_keys(search_keyword)  # 검색어 입력
search_box.send_keys(Keys.ENTER)  # Enter 키 입력으로 검색
driver.implicitly_wait(wait_time)  # 검색 결과 로딩 대기

# wait = input()

# 4. 검색 결과 크롤링
results = []
# for i in range(1, 10):  # 1~10개의 결과를 가져옴
try:
    iframe = driver.find_element(By.ID, f"entryIframe")
    # print(iframe.text)
    driver.switch_to.frame(iframe)

    try:
        # name = driver.find_element(By.XPATH, f"/html/body/div[3]/div/div/div/div[2]/div[1]/div[1]").text
        name = driver.find_element(By.CLASS_NAME, f"GHAhO").text
    except Exception as e:
        name = "장소 정보 없음"
        print(f"Error fetching result name: {e}")

    try:
        btn = driver.find_element(By.CLASS_NAME, "y6tNq").find_element(By.CLASS_NAME, "_UCia")
        btn.click()

        elems = driver.find_elements(By.CLASS_NAME, f"vV_z_")
        for i in range(len(elems)):
            if elems[i].text.startswith("영업 종료"):
                hours = elems[i].text
                break
        address = elems[0].text

        tmp = hours.split('\n')
        hours = "\n".join(tmp[3:-2])

        tmp = address.split('\n')
        address = tmp[0]
    except Exception as e:
        address = "위치 정보 없음"
        hours = "영업시간 정보 없음"
        print(f"Error fetching result address: {e}")

    # 업종 유형 선택자 (필요시 요소 확인 후 수정)
    try:
        # business_type = driver.find_element(By.CSS_SELECTOR, f"/html/body/div[3]/div/div/div/div[2]/div[1]/div[1]/div/span[2]").text
        business_type = driver.find_element(By.CLASS_NAME, f"lnJFt").text
    except Exception as e:
        business_type = "업종 정보 없음"
        print(f"Error fetching result type: {e}")

    results.append((name, address, hours, business_type))

    # 5. 결과 출력
    for result in results:
        print("이름:", result[0])
        print("주소:", result[1])
        print("영업시간:", result[2])
        print("업종 유형:", result[3])
        print("-----------")
except Exception as e:
    print(f"Error fetching result iframe: {e}")
finally:
    # 6. 브라우저 종료
    driver.quit()
