# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import lxml

from construction_comp.items import ConstructionCompItem


class JzscSpider(scrapy.Spider):
    name = "jzsc"
    # allowed_domains = ["http://jzsc.mohurd.gov.cn"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        requestlist = []
        for i in range(1):
            # formdata的value必须是string!
            requestlist.append(scrapy.FormRequest(r'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list',
                                                  formdata={'$pg': str(i+1)}, callback=self.parse_urllist,
                                                  method='POST', headers=self.headers))
        return requestlist

    def parse_urllist(self, response):
        comp_hreflist = response.xpath("//td[@data-header='企业名称']/a/@href").extract()
        for href in comp_hreflist:
            url = r'http://jzsc.mohurd.gov.cn' + href
            yield scrapy.Request(url, callback=self.parse_comp, headers=self.headers)

    def parse_comp(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        comp = ConstructionCompItem()
        comp['name'] = soup('div', class_='user_info spmtop')[0].b.contents[-1].strip()
        # comp['name'] = response.xpath("//div[@class='user_info spmtop']/b/text()").extract()[0].strip()
        # comp['id'] = soup('td', attrs={'data-header': '统一社会信用代码'})[0].string
        comp['adress'] = soup('td', attrs={'data-header': '企业注册属地'})[0].string
        comp['lrp'] = soup('td', attrs={'data-header': '企业法定代表人'})[0].string
        yield comp
