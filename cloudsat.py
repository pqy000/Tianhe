# -*- coding:utf-8 -*-
import ftplib
import os
from time import *


link = 'ftp://waterdata:qhujsj@49.209.80.36'

HOST = 'ftp.nsmc.org.cn'
log = 'A201710160010171291'
pas = '3475'
print log, pas

try:
    f = ftplib.FTP()
    f.connect(HOST)
    f.login(log, pas)
    print('FTP连接成功!')
except:
    print('FTP连接失败!')

sleep(3)

# f.nlst()返回一个当前目录下的列表返回给downloadlist
downloadlist = f.nlst()

if os._exists('data'):
    os.remove('data')
    os.mkdir('./data')

os.chdir('./data')

try:
    for FILE in downloadlist:
        f.retrbinary('RETR %s' % FILE, open(FILE, 'wb').write)
        print('文件"%s"下载成功' % FILE)
except ftplib.error_perm:
    print('无法读取"%s"' % FILE)
    os.unlink(FILE)
else:
    print('文件全部下载完毕！')
    f.quit()