from selenium import webdriver
from PIL import Image
import time
import datetime
import os
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def screenshot_wenshu(query, out_dir, page_delay=5, input_delay=2, search_delay=5, resize_window_delay=2):
    driver = webdriver.Safari()
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    driver.get(url='https://wenshu.court.gov.cn')
    time.sleep(page_delay)  # 等待页面渲染

    #  —————— 登录 ————————
    # 进入登录页面
    driver.find_element(By.XPATH, '//*[@id="loginLi"]/a').click()
    text = driver.page_source
    time.sleep(page_delay)  # 等待页面渲染

    # 自动登录
    # 进入iframe框
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)

    username = driver.find_element(By.XPATH, '//*[@class="phone-number-input"]')
    username.send_keys('username')
    time.sleep(input_delay)
    password = driver.find_element(By.XPATH, '//*[@class="password"]')
    password.send_keys('password')
    time.sleep(input_delay)

    driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div/div[3]/span').click()
    time.sleep(page_delay)

    driver.switch_to.default_content() # 切换回首页
    search = driver.find_element(By.XPATH, '//div[@class="search-middle"]/input')
    search.clear()
    search.send_keys(query)
    time.sleep(input_delay)
    driver.find_element(By.XPATH, '//div[@class="search-rightBtn search-click"]').click()
    time.sleep(search_delay)

    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.set_window_size(width, height) #修改浏览器窗口大小
    time.sleep(resize_window_delay)

    driver.get_screenshot_as_file(out_dir)


def multi_screenshot_wenshu(queries, out_path, page_delay=8, input_delay=2, search_delay=10, resize_window_delay=2, query_delay=8):
    op = Options()
    op.page_load_strategy = 'normal'
    # 隐藏 正在受到自动软件的控制 这几个字
    op.add_experimental_option("excludeSwitches", ["enable-automation"])
    op.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Safari()
    # driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=op)
    # 修改 webdriver 值
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    # })

    driver.maximize_window()
    # driver.set_page_load_timeout(30)
    driver.get(url='https://wenshu.court.gov.cn')
    driver.maximize_window()
    time.sleep(page_delay)  # 等待页面渲染

    #  —————— 登录 ————————
    # 进入登录页面
    driver.find_element(By.XPATH, '//*[@id="loginLi"]/a').click()
    # text = driver.page_source
    time.sleep(page_delay)  # 等待页面渲染

    # 自动登录
    # 进入iframe框
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)
    driver.maximize_window()

    # element = WebDriverWait(driver, 15).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@class="phone-number-input"]')))
    username = driver.find_element(By.XPATH, '//*[@class="phone-number-input"]')
    username.send_keys('username')
    time.sleep(input_delay)
    password = driver.find_element(By.XPATH, '//*[@class="password"]')
    password.send_keys('password')
    time.sleep(input_delay)
    driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div/div[3]/span').click()
    time.sleep(page_delay)

    driver.switch_to.default_content() # 切换回首页
    time.sleep(page_delay)
    for i in range(len(queries)):
        driver.maximize_window()
        search = driver.find_element(By.XPATH, '//div[@class="search-middle"]/input')
        search.clear()
        search.send_keys(queries[i])
        time.sleep(input_delay)
        driver.find_element(By.XPATH, '//div[@class="search-rightBtn search-click"]').click()
        time.sleep(search_delay)

        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width, height) #修改浏览器窗口大小
        time.sleep(resize_window_delay)

        driver.get_screenshot_as_file(os.path.join(out_path, str(i+1) + '-' + queries[i] + '.png'))
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@id="clear-Btn"]').click()
        time.sleep(query_delay)


if __name__ == '__main__':
    current_time = str(datetime.datetime.now())
    out_path = os.path.join('result', current_time)
    os.makedirs(out_path, exist_ok=True)

    # i = 0
    # while i < 3:
    #     print('***********************')
    #     query = input('请输入裁判文书网搜索内容：')
    #     try:
    #         out_dir = os.path.join(out_path, str(i+1) + '-' + query + '.png')
    #         screenshot_wenshu(query=query, out_dir=out_dir)
    #         print('截图保存完成')
    #         i += 1
    #     except Exception as e:
    #         print(e)
    #         print('搜索失败，请重新输入')

    queries = []
    for i in range(3):
        print('***********************')
        query = input('请输入裁判文书网搜索内容' + str(i+1) + ': ')
        queries.append(query)
    while True:
        try:
            multi_screenshot_wenshu(queries=queries, out_path=out_path)
            break
        except Exception as e:
            print(e)
            print('********* Retry *********')
            time.sleep(5)
