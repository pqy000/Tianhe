# -*- coding:utf-8 -*-
from selenium import webdriver
import requests
import urllib2
from time import *
from PIL import Image
from pytesseract import *
import signal

def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table
def login(name, password):
    while 1:
        try:
            elem_usr = driver.find_element_by_id("TextBox_UserID")
            elem_psw = driver.find_element_by_id("TextBox_Psw")
        except:
            break

        driver.find_element_by_id("TextBox_UserID").clear()
        driver.find_element_by_id("TextBox_Psw").clear()
        driver.find_element_by_id("TextBox_Code").clear()
        #继续登陆传值
        driver.find_element_by_id("TextBox_UserID").send_keys(name)
        driver.find_element_by_id("TextBox_Psw").send_keys(password)
        test = raw_input('请输入验证码:')
        try:
            driver.find_element_by_id("TextBox_Code").send_keys(test)
            driver.find_element_by_id("ImageButton_Login").click()
        except:
            print('登陆异常')

    print '登陆成功'

def opt(fr, to, flag):
    sleep(2)
    try:
        driver.get("http://satellite.nsmc.org.cn/PortalSite/Data/Satellite.aspx")
        sleep(5)
        driver.find_element_by_xpath('//*[@id="FY3X"]/div[2]').click()
        sleep(3)
        driver.find_element_by_xpath('//*[@id="FY3C"]').click()
        sleep(3)
        driver.find_element_by_id('MWRI').click()
        sleep(3)
        driver.find_element_by_xpath('//*[@id="VSM"]').click()
        sleep(3)
        driver.find_element_by_xpath('//*[@id="FY3C_MWRIX_GBAL_L2_VSM_MLT_ESD_YYYYMMDD_POAD_025KM_MS.HDF"]').click()
        sleep(5)
        driver.find_element_by_id('imgSearch').click()
        sleep(5)
        print ('订单选择成功！')
    except:
        print('请检查网络，操作中断')
        return

    driver.switch_to_window(driver.window_handles[1])
    sleep(60)
    try:
        driver.find_element_by_xpath('//*[@id="ckbAll"]').click()
    except:
        print ("今日最大文件数已用完")

    sleep(10)
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Data/ShoppingCart.aspx')
    sleep(3)


    driver.switch_to_window(driver.window_handles[1])

    sleep(15)
    try:driver.find_element_by_id('imgSelectAll2').click()
    except:
        print ("今日最大文件数已用完")

    sleep(10)
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Data/ShoppingCart.aspx')
    sleep(3)
    driver.find_element_by_id('chkIsSendMail').click()
    sleep(3)
    driver.find_element_by_xpath('//*[@id="Form1"]/div[6]/div[1]/div[4]/div[2]/a').click()
    sleep(2)

    print('订单提交成功')

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Sup/User/LoginUser.aspx?')
    login('462360632@qq.com', 'yyc18797323396')
    opt('2017-05-13','2017-05-14',True)
    #opt('2017-06-07s','2017-08-03')
