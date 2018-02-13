# -*- coding:utf-8 -*-
from selenium import webdriver
from PIL import Image
from pytesseract import image_to_string
import signal
import poplib
import email
import re
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import ftplib
from time import *
import os

def screenshot():
    # 设置加载页面超时时间
    driver.set_page_load_timeout(1000)
    # 设置窗口大小
    driver.set_window_size(1200, 800)
    try:
        driver.get_screenshot_as_file('screenshot.png')
        im = Image.open('screenshot.png')
        element = driver.find_element_by_id('ImageButton_Code')

        left = int(element.location['x'])
        top = int(element.location['y'])
        right = left + int(element.size['width'])
        bottom = top + int(element.size['height'])

        print(left, top, right, bottom)

        im = Image.open('screenshot.png')
        #im.show()
        im = im.crop((left, top, right, bottom))
        #im.show('code.png')
        im = im.convert('L')
        val = 70
        binaryImage = im.point(initTable(val), '1')
        test = image_to_string(binaryImage, config='-psm 7')
        i = 1
        while (len(test) != 4 and val >= 40):
            binaryImage = im.point(initTable(val), '1')
            test = image_to_string(binaryImage, config='-psm 7')
            val = val - 3
            i = i + 1

        test = test.replace('-', '')
        test = test.replace(' ', '')
        print test
        return test

    except Exception as e:
        print(e)
        return ''

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
        testCode = screenshot()
        #返回继续登陆
        driver.find_element_by_id("TextBox_UserID").clear()
        driver.find_element_by_id("TextBox_Psw").clear()
        driver.find_element_by_id("TextBox_Code").clear()
        #继续登陆传值
        driver.find_element_by_id("TextBox_UserID").send_keys(name)
        driver.find_element_by_id("TextBox_Psw").send_keys(password)

        try:
            driver.find_element_by_id("TextBox_Code").send_keys(testCode)
            driver.find_element_by_id("ImageButton_Login").click()
        except:
            driver.get_screenshot_as_file('test.jpg')
            im2 = Image.open('test.jpg')
            im2.show()

    print '登陆成功'

def storePic():
    driver.get_screenshot_as_file('test.jpg')
    im2 = Image.open('test.jpg')
    im2.show()

def opt():
    try:
        driver.get("http://satellite.nsmc.org.cn/PortalSite/Data/Satellite.aspx")
        sleep(10)
        driver.find_element_by_css_selector('#EOS > div.sjxzqhanmxzqiehuan').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="divImgL1"]').click()
        sleep(5)
        driver.find_element_by_xpath('//*[@id="AQUA_YYYY_MM_DD_HH_mm_xx.MOD02HKM.hdf"]').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="rdgs"]').click()
        sleep(1)
        currentWin = driver.current_window_handle

        storePic()

        driver.find_element_by_id('imgSearch').click()
        handles = driver.window_handles
        print('订单选择成功！')
        sleep(1)
        try:
            driver.switch_to_window(driver.window_handles[1])
        except:
            print('标签页切换出错')
    except:
        print('请检查网络，操作中断')
        return

    sleep(20)
    storePic()

    try:
        driver.find_element_by_id('ckbAll').click()
        driver.get('http://satellite.nsmc.org.cn/PortalSite/Data/ShoppingCart.aspx')
        sleep(3)
        driver.find_element_by_id('chkIsSendMail').click()
        sleep(3)
        driver.find_element_by_css_selector('#imgSubmit').click()
        print('订单提交成功！')
    except:
        print ("今日最大文件数已用完")

def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

# indent用于缩进显示:
def print_info(msg, indent=0):
    sendMail = ''
    receiveMail = ''
    #发件方 与 收件方

    if indent == 0:
        # 邮件的From, To, Subject存在于根对象上:
        print('')
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')

            if value:
                if header=='Subject':
                    # 需要解码Subject字符串:
                    value = decode_str(value)
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = addr

            #print('\n------\n%s', value)

            if header == 'From':
                sendMail = value
            if header == 'To':
                receiveMail = value

    if (msg.is_multipart()):
        parts = msg.get_payload()
        print_info(parts[0], indent + 1)

    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)
            # 要检测文本编码:
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
                pos = re.findall("data set via (.+?) . Please",content)
                temp = pos[0]
                #其中pos[0]表示为FTP链接
                print temp
                address = 'ftp.nsmc.org.cn'
                loginId = temp[6:25]
                loginPass = temp[26:30]
                print ("%s\n%s\n%s\n" % (address, loginId, loginPass) )
                downLoadFTP(address, loginId, loginPass)
        else:
            # 不是文本,作为附件处理:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def downLoadFTP(address, loginId, loginPass):
    try:
        f = ftplib.FTP()
        f.connect(address)
        f.login(loginId, loginPass)
        print('FTP链接成功')
    except:
        print('FTP链接失败')
    sleep(3)
    downloadlist = f.nlst()
    print(downloadlist)

    try:
        for FILE in downloadlist:
            f.retrbinary('RETR %s' % FILE, open(FILE, 'wb').write)
            # print('文件"%s"下载成功' % FILE)
        sleep(5)
    except ftplib.error_perm:
        print('无法读取"%s"' % FILE)
        os.unlink(FILE)
    else:
        print('文件全部下载完毕！')
        f.quit()

def downloadMail(email, password, pop3_server):
    server = poplib.POP3(pop3_server)
    print(server.getwelcome())
    server.user(email)
    server.pass_(password)
    print('Messages: %s. Size: %s' % server.stat())
    resp, mails, octets = server.list()

    print(mails)
    index = len(mails)
    resp, lines, octets = server.retr(index)
    msg_content = '\r\n'.join(lines)
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)
    print_info(msg)

    server.quit()

if __name__ == '__main__':
    driver = webdriver.PhantomJS()
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Sup/User/LoginUser.aspx?')
    login('qhdx', 'water-data')
    opt()
    email = 'pqy_edu@163.com'
    password = '109291ac'
    pop3_server = 'pop3.163.com'
    downloadMail(email, password, pop3_server)

