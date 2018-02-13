
from selenium import webdriver
from cl import *

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Sup/User/LoginUser.aspx?')
    login('qhdx', 'water-data')