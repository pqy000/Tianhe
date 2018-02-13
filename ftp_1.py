# -*- coding:utf-8 -*-
import ftplib
import os
from time import *

link = 'ftp://ftp.cloudsat.cira.colostate.edu'
HOST = 'ftp.cloudsat.cira.colostate.edu'
log = 'pqy000'
pas = '109291ac'
print log, pas

try:
    f = ftplib.FTP()
    f.connect(HOST)
    f.login(log, pas)
    print('FTP连接成功!')
except:
    print('FTP连接失败!')

try:
    # 得到DIRN的工作目录
    #ftp://ftp.cloudsat.cira.colostate.edu/1B-CPR.P_R04/2017/001/
    f.cwd('1B-CPR.P_R04/2017/001/')
    f.dir()
    l = f.retrlines('LIST')

except ftplib.error_perm:
    print('列出当前目录失败')
    f.quit()
print(f.nlst())

sleep(3)

# f.nlst()返回一个当前目录下的列表返回给downloadlist
downloadlist = f.nlst()

if os._exists('CloudSat'):
    os.remove('CloudSat')
    os.mkdir('./CloudSat')

os.chdir('./CloudSat')
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
