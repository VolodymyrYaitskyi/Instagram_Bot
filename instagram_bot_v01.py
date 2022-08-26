from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random
from selenium.webdriver.common.by import By
from pynput.mouse import Controller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3 as sq

with sq.connect("Instabot.db") as con:
    cur = con.cursor()

def create_table():
    cur.execute(""" CREATE TABLE IF NOT EXISTS LIKE_STATISTICS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DATETIME TEXT,
    NUMBER_OF_LIKED_POSTS INT
    )""")

create_table()

class InstagramBot:

    def __init__(self):
        options = Options()
        options.add_argument(r"user-data-dir=C:\Users\MSI1\AppData\Local\Google\Chrome\User Data")
        chromedriver = Service(r'C:\Users\MSI1\Desktop\chromedriver.exe')
        self.like_area_label_xpath = "//*[@class='_aamw']//*[@class='_abl-']//*[@class='_ab6-']"
        self.like_button_xpath = "//*[@class='_aamw']//*[@class='_abl-' and @type='button']"
        self.browser = webdriver.Chrome(service=chromedriver, options=options)

    def close_browser(self):
        self.browser.close()

    def get_posts_urls(self):
        browser = self.browser
        for _ in range(1):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements(by=By.TAG_NAME, value='a')
        posts_urls = []
        for item in hrefs:
            href = item.get_attribute('href')
            if "/p/" in href:
                posts_urls.append(href)
        print(posts_urls)
        return posts_urls

    def check_like_click_like(self):
        browser = self.browser
        like_area_label_xpath = self.like_area_label_xpath
        like_button_xpath = self.like_button_xpath
        like_count = 0
        try:
            wait = WebDriverWait(browser, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, like_button_xpath)))
            if browser.find_element(by=By.XPATH, value=like_area_label_xpath).get_attribute(
                    'aria-label') == "Не подобається":
                time.sleep(random.randrange(2, 10))
                print('Post already liked ')
            else:
                browser.find_element(by=By.XPATH, value=like_button_xpath).click()
                print('Liked post successfully')
                like_count += 1
                time.sleep(random.randrange(5, 10))
                print(like_count)
        except Exception as ex:
            print(ex)
        time.sleep(10)

    def like_photo_by_hashtag(self, hashtag, numbers_of_posts_to_be_liked):
        try:
            browser = self.browser
            like_area_label_xpath = self.like_area_label_xpath
            like_button_xpath = self.like_button_xpath
            like_count = 0
            url1 = f'https://www.instagram.com/explore/tags/{hashtag}/'
            browser.get(url1)
            time.sleep(3)

            for _ in range(4):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))

            hrefs = browser.find_elements(by=By.TAG_NAME, value='a')
            posts_urls = []
            for item in hrefs:
                href = item.get_attribute('href')
                if "/p/" in href:
                    posts_urls.append(href)
            print(posts_urls)

            for url in posts_urls[0:numbers_of_posts_to_be_liked]:
                browser.get(url)
                wait = WebDriverWait(browser, 10)
                wait.until(EC.presence_of_element_located((By.XPATH, like_button_xpath)))
                if browser.find_element(by=By.XPATH, value=like_area_label_xpath).get_attribute(
                        'aria-label') == "Не подобається":
                    time.sleep(random.randrange(2, 10))
                    print('Post already liked ')
                else:
                    browser.find_element(by=By.XPATH, value=like_button_xpath).click()
                    print('Liked post successfully')
                    like_count += 1
                    time.sleep(random.randrange(80, 120))
                    print(like_count)
            print(like_count, 'Likes')
            cur.execute(f"""INSERT INTO LIKE_STATISTICS
                VALUES
                (Null, datetime('now'), {like_count})
                """)
            con.commit()
            self.close_browser()
        except Exception as ex:
            print(ex)
            self.close_browser()

    def like_my_subscribers(self, number_of_posts_to_be_liked):
        browser = self.browser
        my_acc_url = 'https://www.instagram.com/die.slowforme/following/'
        browser.get(my_acc_url)
        time.sleep(random.randrange(5, 9))

        mouse = Controller()
        mouse.position = (620, 339)
        time.sleep(random.randrange(3, 5))
        for _ in range(15):
            mouse.scroll(0, -5)
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements(by=By.TAG_NAME, value='a')
        users_urls = []
        for item in hrefs:
            href = item.get_attribute('href')
            ignore_href = ['https://www.instagram.com/die.slowforme/', 'https://www.instagram.com/explore/',
                           'https://about.instagram.com/blog/', 'https://developers.facebook.com/docs/instagram']
            if href.count('/') == 4 and href not in ignore_href and href not in users_urls:
                users_urls.append(href)
        print(users_urls)
        print(len(users_urls))

        for user_url in users_urls:
            print(f'Going to like {user_url}')
            browser.get(user_url)
            time.sleep(random.randrange(15, 30))
            posts_urls = self.get_posts_urls()
            for url in posts_urls[:number_of_posts_to_be_liked]:
                browser.get(url)
                time.sleep(random.randrange(5, 10))
                self.check_like_click_like()

my_bot = InstagramBot()
my_bot.like_photo_by_hashtag('nikonphoto', 50)
#my_bot.like_my_subscribers(2)
#