# -*- coding: utf-8 -*-
import scrapy
from topMovies.items import TopmoviesItem

from bs4 import BeautifulSoup
import lxml


class DbtopmoviesSpider(scrapy.Spider):
    name = "dbtopMovies"
    allowed_domains = ["douban.com"]
    # start_urls = ['https://movie.douban.com/top250?start=' + str(x) + '&filter=' for x in range(0, 226, 25)]
    # start_urls = ['https://movie.douban.com/top250?start=25&filter='] 豆瓣屏蔽爬虫 返回403错误
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self): # 以新的的headers提交初始Request
        urls = ['https://movie.douban.com/top250?start=' + str(x) + '&filter=' for x in range(0, 226, 25)]
        for url in urls:
            yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        movie = TopmoviesItem()
        soup = BeautifulSoup(response.body.decode(response.encoding), 'lxml')
        ol = soup.ol
        for li in ol('li'):
            try:
                movie['name'] = li('span')[0].string
                movie['num'] = li('em')[0].string
                info = li('div', class_='bd')[0].p.contents[-1].split('\xa0')
                movie['year'] = info[0].strip()
                movie['areas'] = info[2].split(' ')
                movie['styles'] = info[-1].strip().split(' ')
                yield movie
            except:
                continue
