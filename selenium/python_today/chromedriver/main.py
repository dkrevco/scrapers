from selenium import webdriver
import random
# executable_path = 'C:\\Users\\dkrevco\\PycharmProjects\\scrapers\\selenium\\python_today\\chromedriver\\chromedriver.exe'
# driver = webdriver.Chrome(executable_path=executable_path)

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

import time

options = webdriver.ChromeOptions()
# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
# options.add_argument(f"user-agent={user_agent}")

# user_agent_list = []

useragent = UserAgent()
options.add_argument(f'user-agent={useragent.random}')

url = 'https://www.iport.ru/'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


try:
    driver.get(url=url)
    driver.get_screenshot_as_file('1.png')
    time.sleep(10)
    driver.get(url="https://www.iport.ru/catalog/apple_iphone/")
    driver.save_screenshot('2.png')
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()