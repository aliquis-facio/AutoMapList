# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import instaloader
from instaloader import Post
import os
import shutil
import glob

class Instagram_Bot:
    def __init__(self) -> None:
        # driver's options
        self.driver_options = Options()
        self.driver_options.add_experimental_option(
            "excludeSwitches", ["enable-logging"])
        # self.driver_options.add_argument("headless")

        self.long_wait: int = 7  # sec
        self.short_wait: int = 2  # sec

        # initialize the lastest driver
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.driver_options)
        self.driver.implicitly_wait(self.short_wait)

    def login_instagram(self, username, password):
        self.driver.get('https://www.instagram.com/accounts/login/')
        self.driver.implicitly_wait(self.short_wait)

        # 사용자 이름 및 비밀번호 입력
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        username_input.send_keys(username)
        password_input.send_keys(password)

        # 로그인 버튼 클릭
        login_button = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
        login_button.click()
        self.driver.implicitly_wait(self.long_wait)

        next_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/div/div/div')
        next_button.click()
        self.driver.implicitly_wait(self.short_wait)

    # 저장된 게시물로 이동
    def navigate_to_saved(self, username):
        self.driver.get(f'https://www.instagram.com/{username}/saved/all-posts/')
        self.driver.implicitly_wait(self.short_wait)
        
    # 크롤링 실행
    def scrape_saved_posts(self):
        parent = self.driver.find_element(By.CSS_SELECTOR, 'article > div > div')
        children = parent.find_elements(By.TAG_NAME, 'div')
        post_links = []

        for i in range(len(children)):
            posts = children[i].find_elements(By.TAG_NAME, 'a')

            for post in posts:
                post.click()

                post_writer = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/span/span/div/a')
                print(post_writer.text)
                while(True):
                    t = input()
                    if t != '':
                        break
                    
                close_button = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div')
                close_button.click()
                while(True):
                    t = input()
                    if t != '':
                        break
                
                post_link = post.get_attribute('href')
                post_links.append(post_link)

        return post_links

    def close(self):
        self.driver.quit()

class Instagram_Downloader:
    def __init__(self):
        self.instance = instaloader.Instaloader()
    
    def login(self, username, password):
        self.instance.login(username, password)
    
    def download_post(self, post_id, file_path):
        post = Post.from_shortcode(self.instance.context, post_id)
        self.instance.download_post(post, target=file_path)

    def clear_json_file(self, path):
        for dirpath, dirnames, files in os.walk(path):
            for file in os.scandir(dirpath):
                if file.name.endswith('json.xz'):
                    os.remove(file)

if __name__ == "__main__":
    username = 'pi_is_314'
    password = 'jenych0296!'

    Bot = Instagram_Bot()
    
    Bot.login_instagram(username, password)
    Bot.navigate_to_saved(username)
    post_links = Bot.scrape_saved_posts()
    Bot.close()

    # instance = Instagram_Downloader()
    # instance.login(username, password)
    # for post_link in post_links:
    #     print(post_link)
    #     print(post_link[28:-1])
    #     instance.download_post(post_link[28:-1], f'{post_link[28:-1]}')
    # instance.clear_json_file('.\\Instagram')