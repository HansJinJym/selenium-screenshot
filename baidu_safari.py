from selenium import webdriver
from PIL import Image
import time
import datetime
import os
import base64


def screenshot_baidu(query, out_dir, search_delay=4, resize_window_delay=2):
    # 获得WebDriver对象
    driver = webdriver.Safari()
    # 发起get请求
    driver.get('http://www.baidu.com/')

    # <input id="kw" name="wd" class="s_ipt" value="" maxlength="255" autocomplete="off">
    input_element = driver.find_element('name', 'wd')
    input_element.send_keys(query)
    input_element.submit()
    time.sleep(search_delay)

    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.set_window_size(width, height) #修改浏览器窗口大小
    time.sleep(resize_window_delay)

    driver.get_screenshot_as_file(out_dir)

def multi_screenshot_baidu(queries, out_path, search_delay=4, resize_window_delay=2, query_delay=5):
    # 获得WebDriver对象
    # driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver = webdriver.Safari()
    # 发起get请求
    driver.get('http://www.baidu.com/')

    for i in range(len(queries)):
        driver.maximize_window()

        # <input id="kw" name="wd" class="s_ipt" value="" maxlength="255" autocomplete="off">
        input_element = driver.find_element('name', 'wd')
        input_element.send_keys(queries[i])
        input_element.submit()
        time.sleep(search_delay)

        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width, height) #修改浏览器窗口大小
        time.sleep(resize_window_delay)

        driver.get_screenshot_as_file(os.path.join(out_path, str(i+1) + '-' + queries[i] + '.png'))
        time.sleep(query_delay)

        driver.find_element('name', 'wd').clear()

        # # 直接开启设备模拟
        # driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {'mobile':False, 'width':width, 'height':height, 'deviceScaleFactor': 1})
        # # 执行截图
        # res = driver.execute_cdp_cmd('Page.captureScreenshot', { 'fromSurface': True})
        # # 返回的base64内容写入PNG文件
        # with open(os.path.join(out_path, str(i+1) + '-' + queries[i] + '.png'), 'wb') as f:
        #     img = base64.b64decode(res['data'])
        #     f.write(img)



if __name__ == '__main__':
    current_time = str(datetime.datetime.now())
    out_path = os.path.join('result', current_time)
    os.makedirs(out_path, exist_ok=True)

    # for i in range(3):
    #     print('***********************')
    #     query = input('请输入百度内容：')
    #     out_dir = os.path.join(out_path, str(i+1) + '-' + query + '.png')
    #     screenshot_baidu(query=query, out_dir=out_dir)
    #     print('截图保存完成')

    queries = []
    for i in range(3):
        print('***********************')
        query = input('请输入百度内容' + str(i+1) + ': ')
        queries.append(query)
    multi_screenshot_baidu(queries=queries, out_path=out_path)
