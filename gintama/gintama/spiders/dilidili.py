# -*- coding: utf-8 -*-
import scrapy
from gintama.items import GintamaItem


class DilidiliSpider(scrapy.Spider):
    name = 'dilidili'
    allowed_domains = ['dilidili.wang']
    start_urls = ['http://www.dilidili.wang/anime/gintama/']

    def parse(self, response):
        gintamalist = response.xpath("//div[@class='series area']//tr")[1:]
        gintama = GintamaItem()  # 产生Item实例
        for tr in gintamalist:
            try:
                gintama['episode'] = tr.xpath('td[1]/text()')[0].re(r'\d+')[0]
                gintama['gintamatitle'] = tr.xpath('td[2]/a/text()')[0].extract()
                yield gintama
            except:
                continue
        next_urls = response.xpath("//div[@id='tab-menu']/h2/a[@style='color:#333;']/@href").extract()
        for url in next_urls:
            yield scrapy.Request(url, callback=self.parse_2)

    # 用不一样的函数，防止重复提取第一页内容，产生循环提取。
    def parse_2(self, response):
        gintamalist = response.xpath("//div[@class='series area']//tr")[1:]
        gintama = GintamaItem()
        for tr in gintamalist:
            # try 语句防止和第一页有些不一样而产生异常
            try:
                gintama['episode'] = tr.xpath('td[1]/text()')[0].re(r'[\d.]+')[0]
                gintama['gintamatitle'] = tr.xpath('td[2]/a/text()').extract()[0]
                yield gintama
            except:
                continue
        # 网站代码不规范，283话以后缺少<tr>标签（查看源码），下面补充283话以后
        episode_add = response.xpath("//div[@class='series area']/table/td/text()").re(r'第([\d.]+)话')
        title_add = name = response.xpath("//div[@class='series area']/table/td/a/text()").extract()
        for i in range(len(episode_add)):
            gintama['episode'] = episode_add[i]
            gintama['gintamatitle'] = title_add[i]
            yield gintama

