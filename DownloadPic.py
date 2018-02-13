# -*- coding:utf-8 -*-
import urllib

def cbk(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%' % per

for line in open("target.txt"):
    #print line,
    print line[97:146] + str("正在下载")
    url = line
    local  = 'RadaData/' + str(line[97:146])
    urllib.urlretrieve(url, local, cbk)