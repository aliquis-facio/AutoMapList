# -*- coding: utf-8 -*-

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
from Place import Place

class Crawling:
    wait_time: int = 5
    p = Place()

    def __init__(self) -> None:
        try:
            # set driver options
            self.driver_options = Options()
            self.driver_options.add_experimental_option(
                "excludeSwitches", ["enable-logging"])
            # self.driver_options.add_argument("headless") # WebDriver.py 완성하면 풀기

            # initialize the lastest driver
            self.driver = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=self.driver_options)
            self.driver.implicitly_wait(self.wait_time)
        except Exception as e:
            print("Please try again later")
            print(type(e))

    def set_place(self, input_place: str) -> None:
        self.place = input_place
    
    def naver_map_find(self):
        # set intial page
        naver_map_url = "https://map.naver.com/p?c=15.00,0,0,0,dh"
        self.driver.get(url=naver_map_url)

        # select search bar
        search_bar = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div/div/input')

        # search plcae
        search_bar.send_keys(self.place)
        search_bar.send_keys(Keys.ENTER)

        try:
            # open searched place list url
            place_list_url = self.driver.find_element(By.XPATH, '//*[@id="searchIframe"]').get_attribute('src')
            self.driver.get(url = place_list_url)
            self.driver.implicitly_wait(self.wait_time)

            # get place list
            parent_elem = WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/ul')))
            elems = parent_elem.find_elements(By.TAG_NAME, 'li') # no such elem exception 발생함 -> 왜??? 발생하지??
            for elem in elems:
                detailed_name = elem.find_element(By.CLASS_NAME, 'YwYLL').text
                print(detailed_name)
                # print(elem.get_attribute('innerHTML').find('place_bluelink'))
                # self.driver.execute_script("arguments[0].click();", more_button)
            
        except NoSuchElementException as e:
            print(type(e))

    def kakao_map_find(self):
        # set intial page
        kakao_map_url = "https://map.kakao.com/"
        self.driver.get(url=kakao_map_url)

        # select search bar
        search_bar = self.driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')

        # search plcae
        search_bar.send_keys(self.place)
        search_bar.send_keys(Keys.ENTER)

        try:
            # click '장소 더보기' <- 만약에 '장소 더보기' 버튼이 없다면?
            more_button = self.driver.find_element(By.ID, 'info.search.place.more')
            self.driver.execute_script("arguments[0].click();", more_button)

            # get place list
            elems = self.driver.find_element(By.ID, 'info.search.place.list').find_elements(By.TAG_NAME, 'li')
            return elems
            # 다음 페이지로 넘어가서 다른 장소들 챙겨오기 <- 굳이 더 챙겨와야 할까?? 정확하게 검색하면 누가 스타벅스를 통채로 검색함?
        except NoSuchElementException as e:
            print(type(e))

    def google_map_find(self):
        # set intial page
        google_map_url = "https://www.google.com/maps"
        self.driver.get(url=google_map_url)

        # select search bar
        search_bar = self.driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')

        # search plcae
        search_bar.send_keys(self.place)
        search_bar.send_keys(Keys.ENTER)

        try:
            # get place list
            elems = self.driver.find_elements(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div/div')
            for elem in elems:
                print(elem.text)
            
            # 추가적으로 로딩되는 장소들 챙기기
        except NoSuchElementException as e:
            print(type(e))

    def naver_map_extract(self):
        pass

    def kakao_map_extract(self, web_elem_lst: List):
        try:
            for elem in web_elem_lst:
                click_button = elem.find_element(By.CLASS_NAME, 'head_item clickArea')
                self.driver.execute_script("arguments[0].click();", click_button)
                self.driver.implicitly_wait(self.wait_time)

                # 정보 가져와서 Place 객체에 값 집어넣기
                # Place 객체 리턴하기
        except Exception as e:
            print(type(e))

    def google_map_extract(self):
        pass
    
    def driver_close(self) -> None:
        # self.driver.close() # close this browser
        self.driver.quit()  # close every browser


if __name__ == "__main__":
    ChromeDriver = Crawling()
    ChromeDriver.set_place("스타벅스")
    
    # ChromeDriver.naver_map_find() # 수정 요망...
    k_elem_lst = ChromeDriver.kakao_map_find() # 수정 중...
    ChromeDriver.kakao_map_extract(k_elem_lst)
    # ChromeDriver.google_map_find() # 수정할 예정...
    
    ChromeDriver.driver_close()
