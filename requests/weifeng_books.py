#!/user/bin/env python
#_*_coding:utf-8_*_
import requests
from bs4 import BeautifulSoup
from os import path
import time


def get_text(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


def find_books(html):
    try:
        books_url = {}
        soup = BeautifulSoup(html, 'lxml')
        for p in soup('p', class_='attnm'):
            books_url[p.a.text] = p.a.attrs['href']
        return books_url
    except:
        print("not find bookd")


def download_books(books_dic, dir_path):
    for key, value in books_dic.items():
        try:
            r = requests.get(value)
            with open(path.join(dir_path, key), 'ab') as f:
                f.write(r.content)
            print("get %s from %s" % (key, value))
            time.sleep(2)
        except:
            print("not download %s" % key)

        
def spider_weifeng(url, dir_path):
    url_text = get_text(url)
    books_dic = find_books(url_text)
    download_books(books_dic, dir_path)

