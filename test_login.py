from selenium import webdriver
from PIL import Image
import time
import datetime
import os
import random
from selenium.webdriver.common.by import By

driver = webdriver.Safari()
driver.maximize_window()
driver.set_page_load_timeout(30)
driver.get(url='https://wenshu.court.gov.cn')
time.sleep(5)

#  —————— 登录 ————————
# 进入登录页面
driver.find_element(By.XPATH, '//*[@id="loginLi"]/a').click()
text = driver.page_source
time.sleep(5)  # 等待页面渲染

# 自动登录
# 进入iframe框
iframe = driver.find_element(By.TAG_NAME, 'iframe')
driver.switch_to.frame(iframe)

username = driver.find_element(By.XPATH, '//*[@class="phone-number-input"]')
username.send_keys('username')
time.sleep(3)
password = driver.find_element(By.XPATH, '//*[@class="password"]')
password.send_keys('password')
time.sleep(2)

driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div/div[3]/span').click()
time.sleep(5)

driver.switch_to.default_content() # 切换回首页
search = driver.find_element(By.XPATH, '//div[@class="search-middle"]/input')
search.clear()
search.send_keys('北京')
time.sleep(random.randint(1, 5))
driver.find_element(By.XPATH, '//div[@class="search-rightBtn search-click"]').click()
time.sleep(random.randint(1, 5))

time.sleep(10)