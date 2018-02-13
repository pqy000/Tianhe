# -*- coding:utf-8 -*-
import ftplib
import os

link = 'ftp://waterdata:qhujsj@49.209.80.36:9921/'
HOST = '49.209.80.36'
log = link[6:15]
pas = link[16:22]
print log, pas

while 1:
    try:
        f = ftplib.FTP()
        f.connect(HOST,9921)
        f.login(log, pas)
        print('FTP连接成功!')
    except:
        print('FTP连接失败!')

    f.cwd('1')
    f.dir()
    localfile = '/Users/panqingyi/Desktop/data/FY2G_CFR_MLT_NOM_20161121_1700.hdf)'

    file = open(localfile, 'rb')

    downloadfile = os.path.getsize(localfile)

    if (abs(localfile - downloadfile)/localfile) <= 0.05:
        break

f.storbinary('STOR %s' % os.path.basename(localfile), file)