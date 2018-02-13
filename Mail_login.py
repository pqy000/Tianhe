# -*-coding:utf-8 -*-

import poplib
import email
import re
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import ftplib
from time import *
import os

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

            print('\n------\n%s', value)

            if header == 'From':
                sendMail = value
            if header == 'To':
                receiveMail = value

    if (msg.is_multipart()):
        # 如果邮件对象是一个MIMEMultipart,
        # get_payload()返回list，包含所有的子对象:
        parts = msg.get_payload()
        print_info(parts[0], indent + 1)

        #for n, part in enumerate(parts):
            #print('%spart %s' % ('  ' * indent, n))
            #print('part%s' % (n))
            # 递归打印每一个子对象:
            #print_info(part, indent + 1)
            #print(part)

    else:
        # 邮件对象不是一个MIMEMultipart,
        # 就根据content_type判断:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)
            # 要检测文本编码:
            charset = guess_charset(msg)
            print content
            if charset:
                content = content.decode(charset)
                print content()
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

if __name__ == "__main__":
    # 输入邮件地址, 口令和POP3服务器地址:
    email = 'pqy_edu@163.com'
    password = '109291ac'
    pop3_server = 'pop3.163.com'

    server = poplib.POP3(pop3_server)

    print(server.getwelcome())

    server.user(email)
    server.pass_(password)
    print('Messages: %s. Size: %s' % server.stat())

    resp, mails, octets = server.list()
    # 可以查看返回的列表类似['1 82923', '2 2184', ...]
    print(mails)
    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    resp, lines, octets = server.retr(index)
    # lines存储了邮件的原始文本的每一行,
    msg_content = '\r\n'.join(lines)
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)
    print_info(msg)

    # 可以根据邮件索引号直接从服务器删除邮件:
    # server.dele(index)
    # 关闭连接:
    server.quit()