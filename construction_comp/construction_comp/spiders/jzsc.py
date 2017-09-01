# -*- coding: utf-8 -*-
import scrapy


class JzscSpider(scrapy.Spider):
    name = "jzsc"
    allowed_domains = ["http://jzsc.mohurd.gov.cn/dataservice/query/comp/list"]

    def start_requests(self):
        requestlist = []
        for i in range(5):
            # formdata的value必须是string!
            requestlist.append(scrapy.FormRequest(r'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list',
                                                  formdata={'$pg': str(i+1)}, callback=self.parse_complist,
                                                  method='POST'))
        return requestlist

    def parse_complist(self, response):
        comp_namelist = response.xpath("//td[@data-header='企业名称']/a/text()").extract()
        comp_namelist = list(map(lambda x: x.strip(), comp_namelist))
        print(comp_namelist)
