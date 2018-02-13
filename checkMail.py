# -*-coding:utf-8-*-
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from collector.cl import *
from time import sleep
import ftplib
import os

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

# indent用于缩进显示:
def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

if __name__ == '__main__':
    email = 'pqy_edu@163.com'
    password = '109291ac'
    pop3_server = 'pop3.163.com'

    server = poplib.POP3_SSL(pop3_server)
    print(server.getwelcome())
    server.set_debuglevel(0)

    server.user(email)
    server.pass_(password)

    #print(server.stat())
    resp, mails, octets = server.list()
    print(mails)

    #获取最新的一封邮件
    index = len(mails)
    resp, lines, octets = server.retr(index)

    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8')

    msg = Parser().parsestr(msg_content)
    print(print_info(msg))

    server.quit()


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


fro = 'hello'

if fro == "pqy_edu@163.com":
    driver = webdriver.Chrome()
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Sup/User/LoginUser.aspx?')
    login('qhdx','water-data')
    sleep(2)
    #进行FTP下载
    driver.get('http://satellite.nsmc.org.cn/PortalSite/Ord/MyOrders.aspx')
    Load()