# -*- coding:utf-8 -*-
from selenium import webdriver
from time import *
from PIL import Image
import pytesseract
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

        driver.find_element_by_id("ImageButton_Code").click()
        code_link = driver.find_element_by_id("ImageButton_Code").get_attribute('src')
        print code_link

        js = "window.open(' " + code_link + " ' , '_blank' )" #可以看到是打开新的标签页 不是窗口
        driver.execute_script(js)
        #加载完成
        sleep(2)
        #切换标签
        driver.switch_to_window(driver.window_handles[1])

        driver.save_screenshot('screenshot.png')
        element = driver.find_element_by_tag_name('img')

        im = Image.open('screenshot.png')
        left = im.size[0]/2 - element.size['width']
        right = im.size[0]/2 + element.size['width']
        top = im.size[1]/2 - element.size['height']
        bottom =im.size[1]/2 + element.size['height']

        im = im.crop((left, top, right, bottom))

        im.save('code.png')
        #下载图片并识别
        im = Image.open('code.png')

        im = im.convert('L')
        val = 70
        binaryImage = im.point(initTable(val), '1')
        #binaryImage.show()
        test = pytesseract.image_to_string(binaryImage, config='-psm 7')

        i = 2

        while (len(test) != 4 and val >= 40):
            binaryImage = im.point(initTable(val), '1')
            test = pytesseract.image_to_string(binaryImage, config='-psm 7')
            val = val - 3
            print str('The ')+ str(i) + str('-th try ') + test
            i = i + 1

        test = test.replace('-', '')
        test = test.replace(' ', '')
        print str('The original recognition ') + test
        #返回继续登陆
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
        driver.find_element_by_id("TextBox_UserID").clear()
        driver.find_element_by_id("TextBox_Psw").clear()
        driver.find_element_by_id("TextBox_Code").clear()
        #继续登陆传值
        driver.find_element_by_id("TextBox_UserID").send_keys(name)
        driver.find_element_by_id("TextBox_Psw").send_keys(password)
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
        sleep(2)
        driver.find_element_by_xpath('//*[@id="EOS"]/div[2]').click()
        sleep(5)
        driver.find_element_by_id("AQUA_YYYY_MM_DD_HH_mm_xx.MOD02HKM.hdf").click()
        sleep(2)
        if flag == True:
            driver.find_element_by_name('txtBeginDate').clear()
            driver.find_element_by_name('txtEndDate').clear()
            driver.find_element_by_name('txtBeginDate').send_keys(fr)
            driver.find_element_by_name('txtEndDate').send_keys(to)

        driver.find_element_by_xpath('//*[@id="rdgs"]').click()
        sleep(2)
        driver.find_element_by_id('imgSearch').click()
        sleep(5)
        print ('订单选择成功！')
    except:
        print('请检查网络，操作中断')
        return

    driver.switch_to_window(driver.window_handles[1])

    sleep(15)
    try:
        driver.find_element_by_id('imgSelectAll2').click()
    except:
        print ("今日最大文件数已用完")

    sleep(10)
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Data/ShoppingCart.aspx')
    sleep(2)
    driver.find_element_by_id('chkIsSendMail').click()
    sleep(2)
    driver.find_element_by_css_selector('#imgSubmit').click()
    sleep(2)
    print('订单提交成功')

def screenshot(url, filename):
    driver = webdriver.PhantomJS()
    # 设置加载页面超时时间
    driver.set_page_load_timeout(12)
    # 设置窗口大小
    driver.set_window_size(50, 22)

    try:
        driver.get(url)
        driver.get_screenshot_as_file(filename)
    except:
        return ''
    # 结束 Phantomjs 进程
    finally:
        driver.service.process.send_signal(signal.SIGTERM)
        driver.quit()

if __name__ == '__main__':
    #driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    driver.maximize_window()
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Sup/User/LoginUser.aspx?')
    login('qhdx', 'water-data')
    opt('2017-05-13','2017-05-14',True)
    #opt('2017-06-07','2017-08-03')
