from selenium import webdriver
from PIL import Image
import time

# 获得WebDriver对象
driver = webdriver.Safari()
# 发起get请求
driver.get('http://www.baidu.com/')

# <input id="kw" name="wd" class="s_ipt" value="" maxlength="255" autocomplete="off">
input_element = driver.find_element('name', 'wd')
input_element.send_keys('北京')
input_element.submit()
time.sleep(5)

width = driver.execute_script("return document.documentElement.scrollWidth")
height = driver.execute_script("return document.documentElement.scrollHeight")
driver.set_window_size(width, height) #修改浏览器窗口大小
time.sleep(5)

# 获取整个网页截图
driver.get_screenshot_as_file('webpage.png')
print("整个网页尺寸:height={},width={}".format(height, width))
im = Image.open('webpage.png')
print("截图尺寸:height={},width={}".format(im.size[1],im.size[0]))

