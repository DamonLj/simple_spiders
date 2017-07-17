#!/user/bin/env python
#_*_coding:utf-8_*_
import requests
from bs4 import BeautifulSoup
import bs4

def getHTMLtext(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, 'lxml')
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag): #排除换行符等字符串
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string])

def printUnivList(ulist, num):
    #print('{:^10}\t{:^6}\t{:^10}'.format('排名', '大学', '总分'))
    tplt = '{0:^10}\t{1:{3}^10}\t{2:^10}' #在:和^之间加上chr(12288)（中文空格），表示填充空位时使用的字符。使文本好看
    print(tplt.format('排名', '学校名称', '总分', chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))
    print('Suc' + str(num))

def main():
    uinfo = []
    url = r'http://www.zuihaodaxue.com/zuihaodaxuepaiming2017.html'
    html = getHTMLtext(url)
    ulist = fillUnivList(uinfo, html)
    printUnivList(uinfo, 20)

if __name__ == '__main__':
    main()