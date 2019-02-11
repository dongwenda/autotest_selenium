# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2019/2/11 0:17'
import os
import time

from pages.tools import yamlLocator_to_pageObject

# ?collapsed=Passed,XFailed,Skipped
yamlLocator_to_pageObject()
datetime = time.strftime("%Y_%m_%d_%H_%I_%S", time.localtime(time.time()))

os.system('cd C:/autotest_selenium')
os.system('pytest \
--host=127.0.0.1:4723 --browser=chrome \
--html=./reports/{}report.html --self-contained-html \
-q ./cases/test_baidu.py'.format(datetime))