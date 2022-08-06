# 基于selenium的自动截图

## Environment
- environment.yaml

## Usage
- baidu_safari.py :  模拟Safari浏览器，百度搜索并自动截图
- baidu_chrome.py :  模拟Chrome浏览器，百度搜索并自动截图
- wenshu_safari.py :  模拟Safari浏览器，裁判文书网搜索并自动截图
- wenshu_chrome.py :  模拟Chrome浏览器，裁判文书网搜索并自动截图

## 更新：Chrome和Safari效果对比
- 优缺点对比
    1. 处理网页访问。Chrome可以加入```page_load_strategy```来自定义加载页面方式，可选‘normal’、‘eager’、‘none’，Safari没有这种功能，只能通过```sleep()```来控制等待页面加载时间，效率低并且加载慢时很容易报错，鲁棒性较低
    2. 截长图。Safari可以通过```get_screenshot_as_file()```，将网页借助```set_window_size()```调整到最大之后进行截图即可，此时截的图即为长图，较Chrome简单方便。Chrome无法直接将窗口resize到最大进而截图，需要```execute_cdp_cmd()```进行设备模拟，并且得到的是base64编码，较为复杂
    3. 伪装。Chrome的伪装效果好于Safari，即模拟操作更加“真实”。例如可以通过```op.add_experimental_option```来隐藏“浏览器正在受控制”，还可以借助```execute_cdp_cmd()```修改webdriver的值，避免被发现浏览器正在受到自动控制
- 代码与功能对比
    1. driver。在定义driver对象时，Safari不需指定任何参数，直接调用```webdriver.Safari()```即可。Chrome则需要先下载严格对应浏览器版本的驱动，并需要```webdriver.Chrome("/usr/local/bin/chromedriver")```指定驱动位置
    2. ```driver.maximize_window()```。将当前网页resize至显示器全屏大小，Safari可以使用，Chrome没有作用
    3. ```driver.get_screenshot_as_file()```。Safari可以在resize至最大之后调用进行截屏，此时截的是长图。Chrome调用只会截取显示器大小的窗口，无法直接截取长图
    4. ```driver.execute_cdp_cmd()```。Safari的driver没有此方法，仅适用于Chrome，可以执行Chrome开发。例如修改driver值、隐藏受控制字段、得到截图的base64编码等
- 总结：整体来说，selenium自动控制下，Chrome相对Safari代码结构和方法相对较为复杂，但是功能和鲁棒性要远远强于Safari。因此Chrome更加适合开发使用，并且普适性高，Mac、windows都可以使用

## 实现效果
- 百度界面，直接进行逐一搜索
    1. 控制台先接收若干个字符串
    2. 模拟访问百度搜索页面www.baidu.com，然后自动输入第一个搜索词，点击搜索
    3. 搜索页面进行resize到整张网页大小，然后自动截图，此时截的图是长图，然后保存至指定路径
    4. 将网页大小恢复，重新在搜索栏输入下一个搜索词，再进行搜索
    5. 重复步骤3和4，至所有搜索词全部完成搜索并截图
- 裁判文书网，先进行自动登录，然后进行逐一搜索，且每次搜索完成后需要清除关键字之后再进行下一次搜索
    1. 控制台先接收若干个字符串
    2. 模拟访问裁判文书网，然后自动点击“登录”
    3. 如果登录界面渲染不成功，会重新请求访问，页面渲染成功则自动输入账号密码进行登录
    4. 登录成功后自动跳转回到首页，自动输入第一个搜索词，点击搜索
    5. 搜索页面进行resize到整张网页大小，然后自动截图，此时截的图是长图，然后保存至指定路径
    6. 将网页大小恢复，自动点击清除搜索词，重新在搜索栏输入下一个搜索词，再进行搜索
    7. 重复步骤5和6，至所有搜索词全部完成搜索并截图

## tips
- selenium是一个用于Web应用程序测试的工具，测试可直接运行在浏览器中，就像真正的用户在操作一样，并且支持多种浏览器。框架底层使用JavaScript模拟真实用户对浏览器进行操作。测试脚本执行时，浏览器自动按照脚本代码做出点击，输入，打开，验证等操作
- 利用sleep来防止程序执行过快。裁判文书网等网站具有一些反爬虫机制，如果程序执行过快、操作和访问过快等，会使网站弹出验证码输入框来确定是真人在操作，从而导致代码无法继续执行，甚至出现封禁账号、IP等现象。因此在模拟用户操作时，相邻的操作之间需要用sleep隔开，来使程序自动操作更加“真实”
- 元素定位可以用xpath来实现，非常方便且实现简单，只需检查web页面元素，找到对应的组件以及所属的类，即可通过xpath定位该组件，进而进行一系列操作

## 资料
- [selenium](https://www.byhy.net/tut/auto/selenium/xpath_1/)

## Step
- 在safari浏览器的“开发”栏中，勾选“允许远程自动化”
- 进入/usr/bin/safaridriver，双击safaridriver文件启动（第一次驱动需要启动，后面不需要）
- 百度首页用来输入搜索关键词的组件是```<input id="kw" name="wd" class="s_ipt" value="" maxlength="255" autocomplete="off">```
- 裁判文书网搜索组件```<input type="text" class="searchKey search-inp" placeholder="输入案由、关键词、法院、当事人、律师" data-val="s21">```，不支持爬虫，并且存在很多反爬手段，如必须登录才可以进行查询、发现异常随即弹出验证码窗口等
- 百度可直接通过```find_element()```获得搜索框组件，并输入内容提交搜索，裁判文书网无法获得组件，只能通过xpath定位，且需要进行模拟登录，同时设置多个sleep操作防止被弹出验证码
- selenium.common.exceptions.NoSuchFrameException 需要切换至正确的frame
- XPATH即XML路径语言，用来确定xml文档中某部分的路径，相对css语法选择元素更方便（CSS的id、class等属性语法特殊，xpath语法统一），裁判文书网可以通过xpath定位
    - ```//```表示从当前节点往下寻找所有的后代元素,不管它在什么位置
    - 根据属性来选择元素 通过```[@属性名='属性值']```，例如选择id为west的元素，可以```//*[@id='west']```，其中*表示从全部属性中寻找
    - 根据class来选择，例如选择所有select元素中class为single_choice的元素，可以```//select[@class='single_choice']```
- 从网页检查器里找对应的组件，获取xpath，模拟操作即可