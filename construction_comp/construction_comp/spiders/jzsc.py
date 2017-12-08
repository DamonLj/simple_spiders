# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import lxml

from construction_comp.items import ConstructionCompItem


class JzscSpider(scrapy.Spider):
    name = "jzsc"
    # allowed_domains = ["http://jzsc.mohurd.gov.cn"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    }
    CRAWL_PAGE = 10  # 要抓取的总页面数 现在为 275367 // 15 + 1 = 18358

    def start_requests(self):
        requestlist = []
        for i in range(self.CRAWL_PAGE):
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
        comp = ConstructionCompItem()
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            comp['name'] = soup('div', class_='user_info spmtop')[0].b.contents[-1].strip()
            # comp['name'] = response.xpath("//div[@class='user_info spmtop']/b/text()").extract()[0].strip()
            # comp['id'] = soup('td', attrs={'data-header': '统一社会信用代码'})[0].string
            comp['city'] = soup('td', attrs={'data-header': '企业注册属地'})[0].string
            comp['lrperson'] = soup('td', attrs={'data-header': '企业法定代表人'})[0].string
            comp['adress'] = soup('td', attrs={'data-header': '企业经营地址'})[0].string
            certifications_url = soup('a', attrs={'data-contentid': 'apt_tabcontent'})[0].attrs['data-url']
            members_url = soup('a', attrs={'data-contentid': 'iframe_tab'})[0].attrs['data-url']
        except:
            print(response.url, '产生异常！！！未找到comp。')
        # request的meta参数用于传递数据，在不同的parse中返回同一个item。
        yield scrapy.Request("http://jzsc.mohurd.gov.cn" + certifications_url, callback=self.parse_certifications,
                             headers=self.headers, meta={'item': comp}, priority=-1)
        yield scrapy.Request("http://jzsc.mohurd.gov.cn" + members_url, callback=self.parse_memberspage,
                             headers=self.headers, meta={'item': comp}, priority=-2)

    def parse_certifications(self, response):
        comp = response.meta['item']  # 取出传递的item
        certifications = {}
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            allrows = soup('tr', class_='row')
            for row in allrows:
                certifications_cat = row('td', attrs={'data-header': '资质类别'})[0].string.strip()
                certifications_name = row('td', attrs={'data-header': '资质名称'})[0].string.strip()
                if certifications_cat in certifications:
                    certifications[certifications_cat].append(certifications_name)
                else:
                    certifications[certifications_cat] = []
                    certifications[certifications_cat].append(certifications_name)
        except IndexError:
            print(response.url, '未找到任何certifications！！！')
        comp['certifications'] = certifications

    def parse_memberspage(self, response):
        pagebar = response.xpath("//a[@sf='pagebar']/@*")  # 直接提取不到sf:data属性，提取所有属性去最后一个
        # 如果只有一页不能产生request，因为是重复的url会被过滤掉。
        if not pagebar:
            comp = next(self.parse_members(response))  # 用next取出parse生成器中的item，不能直接返回生成器。
            yield comp
        else:
            comp = response.meta['item']
            page_str = pagebar[-1].extract()
            import re
            total = int(re.search(r'tt:(\d+),', page_str).group(1))
            pagesize = int(re.search(r'ps:(\d+),', page_str).group(1))
            remainder = total % pagesize
            page_num = total // pagesize + 1
            for p in range(page_num - 1):
                yield scrapy.FormRequest(response.url, formdata={'$pg': str(p + 1)}, callback=self.parse_members_none,
                                         method='POST', headers=self.headers,
                                         meta={'item': comp, 'pagesize': pagesize}, priority=-3)
            yield scrapy.FormRequest(response.url, formdata={'$pg': str(page_num)},
                                     callback=self.parse_members_last, method='POST', headers=self.headers,
                                     meta={'item': comp, 'remainder': remainder}, priority=-4)

    def parse_members_last(self, response):
        comp = response.meta['item']
        remainder = response.meta['remainder']
        if 'members' not in comp:
            comp['members'] = {}
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            allmembers = soup('table', class_='pro_table_box pro_table_borderright')[0]('tbody')[0]('tr')
            for member in allmembers[:remainder]:
                member_cat = member('td', attrs={'data-header': '注册类别'})[0].string.strip()
                member_name = member('td', attrs={'data-header': '姓名'})[0].a.string.strip()
                if member_cat in comp['members']:
                    comp['members'][member_cat].append(member_name)
                else:
                    comp['members'][member_cat] = []
                    comp['members'][member_cat].append(member_name)
        except IndexError:
            print(response.url, '未找到任何member!!!!')
        yield comp

    def parse_members_none(self, response):
        comp = response.meta['item']
        pagesize = response.meta['pagesize']
        if 'members' not in comp:
            comp['members'] = {}
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            allmembers = soup('table', class_='pro_table_box pro_table_borderright')[0]('tbody')[0]('tr')
            for member in allmembers[:pagesize]:
                member_cat = member('td', attrs={'data-header': '注册类别'})[0].string.strip()
                member_name = member('td', attrs={'data-header': '姓名'})[0].a.string.strip()
                if member_cat in comp['members']:
                    comp['members'][member_cat].append(member_name)
                else:
                    comp['members'][member_cat] = []
                    comp['members'][member_cat].append(member_name)
        except IndexError:
            print(response.url, '未找到任何member!!!!')

    def parse_members(self, response):
        comp = response.meta['item']
        if 'members' not in comp:
            comp['members'] = {}
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            allmembers = soup('table', class_='pro_table_box pro_table_borderright')[0]('tbody')[0]('tr')
            for member in allmembers:
                member_cat = member('td', attrs={'data-header': '注册类别'})[0].string.strip()
                member_name = member('td', attrs={'data-header': '姓名'})[0].a.string.strip()
                if member_cat in comp['members']:
                    comp['members'][member_cat].append(member_name)
                else:
                    comp['members'][member_cat] = []
                    comp['members'][member_cat].append(member_name)
        except IndexError:
            print(response.url, '未找到任何member!!!!')
        yield comp
