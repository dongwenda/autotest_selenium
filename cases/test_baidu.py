# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2019/2/11 17:37'
from time import sleep

from pages.page_objects import BaiduHomePage

def test_01(handle):
    handle.get("https://www.baidu.com/")
    handle.send_keys(locator=BaiduHomePage.输入框, text='selenium')
    handle.click(locator=BaiduHomePage.搜索按钮)
    sleep(5)
    raise Exception("报错截图")