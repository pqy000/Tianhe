# -*- coding:utf-8 -*-
from selenium import webdriver
from collector.cl import *
from time import sleep
import ftplib
import os

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
        test = image_to_string(binaryImage, config='-psm 7')
        i = 2
        #识别率要求不断增高且控制字符长度为4
        while(len(test) != 4 and val >= 40):
            binaryImage = im.point(initTable(val), '1')
            test = image_to_string(binaryImage, config='-psm 7')
            val = val - 3
            print str('The ')+ str(i) + str('-th try ') + test
            i = i + 1

        #标示最终识别出的字符长度仍然大于4

        test = test.replace('-', '')
        test = test.replace(' ', '')
        test = test.replace(':', '')
        print str('The original recognition ')+test
        #test = raw_input()
        #返回继续登陆
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
        driver.find_element_by_id("TextBox_UserID").clear()
        driver.find_element_by_id("TextBox_Psw").clear()
        driver.find_element_by_id("TextBox_Code").clear()
        #继续登陆传值
        driver.find_element_by_id("TextBox_UserID").send_keys(name)
        driver.find_element_by_id("TextBox_Psw").send_keys(password)
        driver.find_element_by_id("TextBox_Code").send_keys(test)
        driver.find_element_by_id("ImageButton_Login").click()
    print '登陆成功'

#
def Load():
    try:
        ele = driver.find_element_by_xpath('//*[@id="displayOrdersList"]/tbody[2]/tr[1]/td[7]/a')
    except:
        print('当前没有下载链接')
        return
    link = ele.get_attribute('href')
    driver.find_element_by_xpath('//*[@id="displayOrdersList"]/tbody[2]/tr[1]/td[7]/a').click()
    if link != None:
        print '下载链接获取成功'
        log = link[6:25]
        pas = link[26:30]
        HOST = 'ftp.nsmc.org.cn'
        print log, pas
    try:
        f = ftplib.FTP(HOST)
        f.login(log, pas)
        print('FTP连接成功!')
    except:
        print('FTP连接失败!')

    try:
        # 得到DIRN的工作目录
        l = f.retrlines('LIST')
    except ftplib.error_perm:
        print('列出当前目录失败')
        f.quit()

    print(f.nlst())

    # f.nlst()返回一个当前目录下的列表返回给downloadlist
    downloadlist = f.nlst()
    try:
        for FILE in downloadlist:
            f.retrbinary('RETR %s' % FILE, open(FILE, 'wb').write)
            print('文件"%s"正在下载中' % FILE)
            print('文件"%s"下载成功' % FILE)
    except ftplib.error_perm:
        print('无法读取"%s"' % FILE)
        os.unlink(FILE)
    else:
        print('文件全部下载完毕！')
        f.quit()

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Sup/User/LoginUser.aspx?')
    login('qhdx','water-data')
    sleep(2)
    #进行FTP下载
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Ord/MyOrders.aspx')
    Load()

