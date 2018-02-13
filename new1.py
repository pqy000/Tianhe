from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
import requests
import urllib

from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get('http://www.sciencedirect.com/science/article/pii/S002002550900142X/pdfft?md5=67041f2a3f32588f49d5d94b28ffbbf5&pid=1-s2.0-S002002550900142X-main.pdf')
url = driver.current_url
urllib.urlretrieve(url, 'paper.pdf')
