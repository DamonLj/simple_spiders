# -*- coding: utf-8 -*-
import scrapy
from gintama.items import GintamaItem

class DilidiliSpider(scrapy.Spider):
    name = 'dilidili'
    allowed_domains = ['dilidili.wang']
    start_urls = ['http://www.dilidili.wang/anime/gintama/']

    def parse(self, response):
        gintamalist = response.xpath("//div[@class='series area']//tr")[1:]
        gintama = GintamaItem()
        for tr in gintamalist:
            gintama['episode'] = tr.xpath('td[1]/text()').extract()[0]
            gintama['gintamatitle'] = tr.xpath('td[2]/a/text()').extract()[0]
            yield gintama
        nexturls = response.xpath("//div[@id='tab-menu']/h2/a[@style='color:#333;']/@href").extract()
        for url in nexturls:
            yield scrapy.Request(url, callback='parse')