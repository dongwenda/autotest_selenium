from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

class Base:
    '''
    selenium api 封装
    '''
    def __init__(self, logger, driver=None):
        self.driver = driver
        self.timeout = 6
        self.t = 0.5
        self.logger = logger
    
    def _get_driver(self, driver):
        '''获取driver，判断用初始化的driver还是传入的driver，传入的优先级的driver优先级最高'''
        return driver or self.driver

    def _get_element(self, locator, element, driver):
        '''判断传入的是locator还是element；返回element; 只传其中一个'''
        if element:
            return element
        return self.find_element(locator, driver)
    
    def find_element(self, locator, driver=None):
        '''
        定位元素
        返回定位到的元素，没定位到则抛timeout异常
        locator： ('id', 'kw')/('css selector', 'input#kw')
         ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"
        '''
        if not isinstance(locator, tuple):
            self.logger.error('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
            raise Exception('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        driver = self._get_driver(driver)
        try:
            element = WebDriverWait(driver, self.timeout, self.t).until(EC.presence_of_element_located(locator))
            self.logger.info("定位元素信息：定位方式->%s, value值->%s"%(locator[0], locator[1]))
        except Exception:
            self.logger.error("定位方式报错->%s, value值->%s"%(locator[0], locator[1]), exc_info=True)
            #raise Exception("定位方式报错->%s, value值->%s"%(locator[0], locator[1]))
            return False
        else:
            return element

    def find_elements(self, locator, driver=None):
        # 定位元素, 返回元素[]
        if not isinstance(locator, tuple):
            self.logger.error('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
            raise Exception('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        driver = self._get_driver(driver)
        try:
            elements = WebDriverWait(driver, self.timeout, self.t).until(EC.presence_of_all_elements_located(locator))
            self.logger.info("定位元素信息：定位方式->%s, value值->%s"%(locator[0], locator[1]))
            return elements
        except Exception:
            self.logger.error("查找元素报错->%s, value值->%s"%(locator[0], locator[1]), exc_info=True)

    def send_keys(self, locator=None, text='', element=None, driver=None):
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        element.send_keys(text)
        self.logger.info("输入信息：%s"% text)

    def click(self, locator=None, element=None, driver=None):
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        element.click()
        self.logger.info("点击元素")

    def clear(self, locator=None, element=None, driver=None):
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        element.clear()
        self.logger.info("清空输入框")

    def is_selected(self, locator=None, element=None, driver=None):
        '''判断元素是否被选中，返回bool值'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        r = element.is_selected()
        self.logger.info("元素是否被选中:%s" %r)
        return r

    def is_enabled(self, locator=None, element=None, driver=None):
        '''判断input\select等元素是否可编辑状态，返回bool值'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        r = element.is_enabled()
        self.logger.info("元素是否可编辑：%s" %r)
        return r

    def is_element_exist(self, locator=None, element=None, driver=None):
        '''判断元素是否存在，返回bool值'''
        driver = self._get_driver(driver)
        try:
            self._get_element(locator, element, driver)
            self.logger.info("元素存在")
            return True
        except:
            self.logger.info("元素不存在")
            return False

    def is_title(self, title='', driver=None):
        '''判断标题是否相同，返回bool'''
        driver = self._get_driver(driver)
        try:
            result = WebDriverWait(driver, self.timeout, self.t).until(EC.title_is(title))
            self.logger.info('标题相同：%s'%title)
            return result
        except:
            self.logger.info('标题不相同：%s' % title)
            return False

    def is_title_contains(self, title='', driver=None):
        '''判断标题是否包含，返回bool'''
        driver = self._get_driver(driver)
        try:
            result = WebDriverWait(driver, self.timeout, self.t).until(EC.title_contains(title))
            self.logger.info('标题包含：%s' % title)
            return result
        except:
            self.logger.info('标题没有包含：%s' % title)
            return False

    def is_element_contains_text(self, locator, text='', driver=None):
        '''判断元素是否包含预期的字符串，返回bool'''
        if not isinstance(locator, tuple):
            self.logger.error('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
            raise Exception('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        driver = self._get_driver(driver)
        try:
            result = WebDriverWait(driver, self.timeout, self.t).until(EC.text_to_be_present_in_element(locator, text))
            self.logger.info('元素文本值包含：%s'%text)
            return result
        except:
            self.logger.info('元素文本值没有包含：%s' % text)
            return False

    def is_elementValue_contains_value(self, locator, value='', driver=None):
        '''判断元素的value属性值是否包含预期的value，返回bool'''
        if not isinstance(locator, tuple):
            self.logger.error('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
            raise Exception('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        driver = self._get_driver(driver)
        try:
            result = WebDriverWait(driver, self.timeout, self.t).until(EC.text_to_be_present_in_element_value(locator, value))
            self.logger.info('元素的value属性值包含：%s'%value)
            return result
        except:
            self.logger.info('元素的value属性值没有包含：%s' % value)
            return False

    def is_alert(self, timeout=3, driver=None):
        '''判断alert,存在返回alert实例，不存在，返回false'''
        driver = self._get_driver(driver)
        try:
            result = WebDriverWait(driver, timeout, self.t).until(EC.alert_is_present())
            self.logger.info('有alert弹框')
            return result
        except:
            self.logger.info('没有alert弹框')
            return False

    def get(self, url, driver=None):
        '''打开地址'''
        driver = self._get_driver(driver)
        driver.get(url)
        self.logger.info('打开url：%s'%url)

    def refresh(self, driver=None):
        '''刷新页面'''
        driver = self._get_driver(driver)
        driver.refresh()
        self.logger.info('刷新页面')

    def forward(self, driver=None):
        '''跳转到下一页'''
        driver = self._get_driver(driver)
        driver.forward()
        self.logger.info('跳转下一页')

    def back(self, driver=None):
        '''跳转到下一页'''
        driver = self._get_driver(driver)
        driver.back()
        self.logger.info('跳转上一页')

    def maximize_window(self, driver=None):
        '''最大化浏览器'''
        driver = self._get_driver(driver)
        driver.maximize_window()
        self.logger.info('最大化浏览器')

    def set_window_size(self, x=100, y=50, driver=None):
        '''设置窗口大小'''
        driver = self._get_driver(driver)
        driver.set_window_size(x, y)
        self.logger.info('设置窗口大小%s，%s'%(x, y))

    def set_page_load_timeout(self, timeout=15, driver=None):
        '''设置页面加载超时时间'''
        driver = self._get_driver(driver)
        driver.set_page_load_timeout(timeout)
        self.logger.info('设置页面加载超时时间：%s' %timeout)

    def close(self, driver=None):
        '''关闭浏览器'''
        driver = self._get_driver(driver)
        driver.quit()
        self.logger.info('关闭浏览器')

    def get_screenshot(self, file_path, driver=None):
        '''截图;  file_path="/pictures/test.png" '''
        driver = self._get_driver(driver)
        driver.get_screenshot_as_file(file_path)
        self.logger.info('截图：%s'%file_path)

    def get_cookies(self, driver=None):
        '''获取所有cookies'''
        driver = self._get_driver(driver)
        cookies = driver.get_cookies()
        self.logger.info('获取所有cookies信息：%s' %cookies)
        return cookies

    def get_cookie(self, name, driver=None):
        '''获取cookies的某个值'''
        driver = self._get_driver(driver)
        cookie = driver.get_cookie(name)
        self.logger.info('获取%s的cookie信息：%s' %(name, cookie))
        return cookie

    def delete_cookie(self, name, driver=None):
        '''删除指定的cookie信息'''
        driver = self._get_driver(driver)
        driver.delete_cookie(name)
        self.logger.info('删除%s的cookie信息' %name)

    def delete_cookies(self, driver=None):
        '''删除所有的cookies信息'''
        driver = self._get_driver(driver)
        driver.delete_all_cookies()
        self.logger.info('删除所有的cookie信息')

    def add_cookie(self, cookie_dict, driver=None):
        '''添加cookies信息'''
        driver = self._get_driver(driver)
        driver.add_cookie(cookie_dict)
        self.logger.info('添加cookies信息：%s' %cookie_dict)

    def get_title(self, driver=None):
        '''获取title标题'''
        driver = self._get_driver(driver)
        title = driver.title
        self.logger.info('获取标题：%s'%title)
        return title

    def get_url(self, driver=None):
        '''获取当前url'''
        driver = self._get_driver(driver)
        url = driver.current_url
        self.logger.info('获取当前url：%s' % url)
        return url

    def get_element_text(self, locator=None, element=None, driver=None):
        '''获取元素的文本'''
        try:
            driver = self._get_driver(driver)
            element = self._get_element(locator, element, driver)
            text = element.text
            self.logger.info('获取元素的文本：%s'%text)
            return text
        except:
            self.logger.info("获取text失败，返回''")
            return ""

    def get_element_attribute(self, locator, name, element=None, driver=None):
        '''获取元素的属性'''
        driver = self._get_driver(driver)
        try:
            element = self._get_element(locator, element, driver)
            attribute = element.get_attribute(name)
            self.logger.info('获取元素的%s属性：' %(name,attribute))
            return attribute
        except:
            self.logger.info("获取元素的%s属性失败，返回''")
            return ""

    def js_focus_element(self, locator=None, element=None, driver=None):
        '''聚焦元素'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        driver.execute_script("arguments[0].scrollIntoView();", target_element)
        self.logger.info("聚焦元素")

    def js_scroll_top(self, driver=None):
        '''滚动到顶部'''
        driver = self._get_driver(driver)
        js = "window.scrollTo(0,0)"
        driver.execute_script(js)
        self.logger.info("滚动到顶部")

    def js_scroll_end(self, x=0, driver=None):
        '''滚动到底部'''
        driver = self._get_driver(driver)
        js = "window.scrollTo(%s,document.body.scrollHeight)" % x
        driver.execute_script(js)
        self.logger.info("滚动到底部")

    def js_play_video(self, locator=None, element=None, driver=None):
        '''播放视频'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        js = "arguments[0].play();"
        driver.execute_script(js, target_element)
        self.logger.info("播放视频")

    def select_by_index(self, locator, index=0, element=None, driver=None):
        '''下拉框，通过索引选择。index是索引第几个，从0开始，默认选第一个'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        Select(target_element).select_by_index(index)
        self.logger.info("下拉框选择索引%s的值"%index)

    def select_by_value(self, locator, value, element=None, driver=None):
        '''下拉框，通过value选择'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        Select(target_element).select_by_value(value)
        self.logger.info("下拉框选择value:%s的值"%value)

    def select_by_text(self, locator, text, element=None, driver=None):
        '''下拉框，通过文本值选择'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        Select(target_element).select_by_visible_text(text)
        self.logger.info("下拉框选择文本:%s的值" % text)

    def deselect_by_index(self, locator, index=0, element=None, driver=None):
        '''下拉框，通过索引,取消选择。index是索引第几个，从0开始，默认取消第一个'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        Select(target_element).deselect_by_index(index)
        self.logger.info("下拉框取消选择索引%s的值" % index)

    def deselect_by_value(self, locator, value, element=None, driver=None):
        '''下拉框，通过value，取消选择'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        Select(target_element).deselect_by_index(value)
        self.logger.info("下拉框取消选择value:%s的值"%value)

    def deselect_by_text(self, locator, text, element=None, driver=None):
        '''下拉框，通过文本值，取消选择'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        Select(target_element).deselect_by_visible_text(text)
        self.logger.info("下拉框取消选择文本:%s的值" % text)

    def deselect_all(self, locator=None, element=None, driver=None):
        '''下拉框，取消选择'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        Select(target_element).deselect_all()
        self.logger.info("下拉框取消选择")

    def get_select_options(self, locator=None, element=None, driver=None):
        '''获取下拉框的所有options ； 遍历之后 .text可以获取该文本值'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        options = Select(target_element).options()
        self.logger.info("获取下拉框的所有options")
        return options

    def get_first_selected_option(self, locator=None, element=None, driver=None):
        '''获取第一个被选中的option'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        first_option = Select(target_element).first_selected_option()
        self.logger.info("获取下拉框的第一个被选中的option")
        return first_option

    def get_selected_options(self, locator=None, element=None, driver=None):
        '''获取所有被选中的option'''
        driver = self._get_driver(driver)
        target_element = self._get_element(locator, element, driver)
        options = Select(target_element).all_selected_options()
        self.logger.info("获取下拉框的所有被选中的option")
        return options

    def switch_iframe(self, id_name_index_locator, driver=None):
        '''切换iframe ； 可以传入id、name、index以及selenium的WebElement对象'''
        driver = self._get_driver(driver)
        try:
            if isinstance(id_name_index_locator, tuple):
                element = self.find_element(id_name_index_locator)
                driver.switch_to.frame(element)
            driver.switch_to.frame(id_name_index_locator)
            self.logger.info("切换iframe")
        except:
            self.logger.error("切换iframe异常", exc_info=True)
            raise Exception("切换iframe异常")

    def switch_default_content(self, driver=None):
        '''释放iframe'''
        driver = self._get_driver(driver)
        driver.switch_to.default_content()
        self.logger.info("释放iframe")

    def switch_parent_iframe(self, driver=None):
        '''回到父级的iframe'''
        driver = self._get_driver(driver)
        driver.switch_to.parent_frame()
        self.logger.info("回到父级的iframe")

    def get_current_handle(self, driver=None):
        '''获取当前句柄窗口'''
        driver = self._get_driver(driver)
        handle = driver.current_window_handle()
        self.logger.info("获取当前句柄窗口")
        return handle

    def get_handles(self, driver=None):
        '''获取所有的句柄窗口'''
        driver = self._get_driver(driver)
        handles = driver.window_handles()
        self.logger.info("获取所有的句柄窗口")
        return handles

    def switch_handle(self, handle, driver=None):
        '''切换句柄窗口'''
        driver = self._get_driver(driver)
        driver.switch_to.window(handle)
        self.logger.info("切换句柄窗口")

    def switch_alert(self, driver=None):
        '''切换到alert ；'''
        driver = self._get_driver(driver)
        alert = driver.switch_to_alert()
        self.logger.info("切换到alert")
        return alert

    def accept_alert(self, driver=None):
        '''切换到alert ； 并且点击确认'''
        self.switch_alert(driver).accept()
        self.logger.info("点击确认alert")

    def dismiss_alert(self, driver=None):
        '''切换到alert ； 并且点击取消'''
        self.switch_alert(driver).dismiss()
        self.logger.info("点击取消alert")

    def execute_js(self, js, driver=None):
        '''执行js脚本'''
        driver = self._get_driver(driver)
        driver.execute_script(js)
        self.logger.info("执行js脚本--> %s"%js)

    def move_to_element(self, locator=None, element=None, driver=None):
        '''鼠标悬停到某个元素上'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        ActionChains(driver).move_to_element(element).perform()
        self.logger.info("鼠标悬停到元素上")

    def double_click(self, locator=None, element=None, driver=None):
        '''双击鼠标'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        ActionChains(driver).double_click(element).perform()
        self.logger.info("双击鼠标")

    def context_click(self, locator=None, element=None, driver=None):
        '''点击鼠标右键'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        ActionChains(driver).context_click(element).perform()
        self.logger.info("点击鼠标右键")

    def drag_element(self, from_locator, to_locator, driver=None):
        '''拖动元素（原元素--->目标元素）'''
        driver = self._get_driver(driver)
        from_element = self.find_element(from_locator, driver)
        to_element = self.find_element(to_locator, driver)
        ActionChains(driver).drag_and_drop(from_element, to_element).perform()
        self.logger.info("拖动元素")




if __name__ == '__main__':
    from selenium import webdriver
    from time import sleep
    from selenium.webdriver.chrome.options import Options
    from logger import Logger

    logger = Logger()

    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    handle = Base(logger=logger, driver=driver) # logger是必传的，driver可以不传
    handle.maximize_window()
    handle.set_page_load_timeout()
    handle.get('http://www.baidu.com')
    handle.send_keys(('id', 'kw'), '哦哦哦哦')  # 初始化传了driver的，默认用初始化的driver
    sleep(1)

    handle.clear(('id', 'kw'), driver=driver)   # 初始化没有传driver，或者传了driver的；调方法时，传driver会优先用方法传的driver

    sleep(2)
    search_btn_ele = handle.find_element(('id', 'su'))
    handle.double_click(element=search_btn_ele) # 可以传locator或者element，其中一个，去操作
    sleep(2)
    handle.close()

