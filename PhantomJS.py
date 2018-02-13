# -*- coding:utf-8 -*-
from selenium import webdriver
import requests
import urllib2
from time import *
from PIL import Image
from pytesseract import *
import signal

def screenshot(url):
    driver = webdriver.PhantomJS()
    # 设置加载页面超时时间
    driver.set_page_load_timeout(20)
    # 设置窗口大小
    driver.set_window_size(1200, 800)

    try:
        cookies = driver.get_cookies()
        for k, v in enumerate(cookies):
            cookie_dict = {'name': k, 'value': v}
            driver.add_cookie(cookie_dict)
        driver.get(url)
        driver.get_screenshot_as_file('screenshot.png')

        frame = driver.find_element_by_css_selector('iframe#changeCodeImg')
        frame_left = int(frame.location['x'])  # 获取iframe的坐标
        frame_top = int(frame.location['y'])

        driver.switch_to.frame("changeCodeImg")  # 切换到iframe中
        element = driver.find_element_by_css_selector('input#imgCode')  # 找到验证码的element
        left = frame_left + int(element.location['x'])
        top = frame_top + int(element.location['y'])
        right = frame_left + int(element.location['x'] + element.size['width'])
        bottom = frame_top + int(element.location['y'] + element.size['height'])

        print(left, top, right, bottom)
        # 通过Image处理图像

        im = Image.open('screenshot.png')
        im.show()
        im = im.crop((left, top, right, bottom))
        im.show('code.png')

    except Exception as e:
        print(e)
        return ''
    # 结束 Phantomjs 进程
    finally:
        driver.service.process.send_signal(signal.SIGTERM)
        driver.quit()


if __name__ == "__main__":
    screenshot("http://satellite.nsmc.org.cn/portalsite/default.aspx")