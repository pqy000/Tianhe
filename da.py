# -*- coding:utf-8 -*-
from selenium import webdriver
import requests
import urllib2
from time import *
from PIL import Image
from pytesseract import *


driver = webdriver.Chrome()

driver.get("http://satellite.nsmc.org.cn/PortalSite/Sup/User/LoginUser.aspx?")


try:
    elem_usr = driver.find_element_by_id("TextBox_UserID")
    elem_psw = driver.find_element_by_id("TextBox_Psw")
except:
    print('网络延迟')

driver.find_element_by_id("TextBox_UserID").clear()
driver.find_element_by_id("TextBox_Psw").clear()
driver.find_element_by_id("TextBox_Code").clear()

test = raw_input()

driver.find_element_by_id("TextBox_UserID").send_keys("qhdx")
driver.find_element_by_id("TextBox_Psw").send_keys("water-data")
driver.find_element_by_id("TextBox_Code").send_keys(test)

driver.find_element_by_id("ImageButton_Login").click()