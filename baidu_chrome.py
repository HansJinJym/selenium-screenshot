from selenium import webdriver
from PIL import Image
import time
import datetime
import os
import base64

def multi_screenshot_baidu(queries, out_path, search_delay=4, resize_window_delay=2, query_delay=5):
    # 获得WebDriver对象
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    # driver = webdriver.Safari()
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
        
        # 直接开启设备模拟
        driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {'mobile':False, 'width':width, 'height':height, 'deviceScaleFactor': 1})
        # 执行截图
        res = driver.execute_cdp_cmd('Page.captureScreenshot', { 'fromSurface': True})
        # 返回的base64内容写入PNG文件
        with open(os.path.join(out_path, str(i+1) + '-' + queries[i] + '.png'), 'wb') as f:
            img = base64.b64decode(res['data'])
            f.write(img)
        time.sleep(resize_window_delay)

        driver.find_element('name', 'wd').clear()
        driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {'mobile':False, 'width':1400, 'height':1000, 'deviceScaleFactor': 1})
        time.sleep(query_delay)



if __name__ == '__main__':
    current_time = str(datetime.datetime.now())
    out_path = os.path.join('result', current_time)
    os.makedirs(out_path, exist_ok=True)

    queries = []
    for i in range(3):
        print('***********************')
        query = input('请输入百度内容' + str(i+1) + ': ')
        queries.append(query)
    multi_screenshot_baidu(queries=queries, out_path=out_path)
