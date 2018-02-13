
from selenium import webdriver
import requests
import urllib2
from time import *
from PIL import Image
from pytesseract import *
from cl import login

driver = webdriver.Chrome()

driver.maximize_window()
driver.get('http://satellite.nsmc.org.cn/PortalSite/Sup/User/LoginUser.aspx?')

login('qhdx','water-data')

sleep(2)

driver.get("http://satellite.nsmc.org.cn/PortalSite/Data/Satellite.aspx")

sleep(2)

driver.find_element_by_xpath('//*[@id="EOS"]/div[2]').click()

sleep(5)

driver.find_element_by_id("AQUA_YYYY_MM_DD_HH_mm_xx.MOD02HKM.hdf").click()

sleep(2)

driver.find_element_by_xpath('//*[@id="rdgs"]').click()

sleep(2)

driver.find_element_by_id('imgSearch').click()

sleep(5)

driver.switch_to_window(driver.window_handles[1])

#driver.get('http://satellite.nsmc.org.cn/PortalSite/Data/FileShow.aspx')

sleep(5)

try:
    driver.find_element_by_id('imgSelectAll2').click()
except :
    print ("345")

sleep(5)

driver.get('http://satellite.nsmc.org.cn/PortalSite/Data/ShoppingCart.aspx')

sleep(5)

driver.find_element_by_id('chkIsSendMail').click()

sleep(3)
'''
try:
    driver.find_element_by_id('imgSubmit').click()
except:
    print ("123")
'''

driver.find_element_by_xpath('//*[@id="Form1"]/div[6]/div[1]/div[4]/div[2]/a').click()

sleep(2)

#driver.get('http://satellite.nsmc.org.cn/PortalSite/Ord/MyOrders.aspx')

