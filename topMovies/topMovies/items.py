# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TopmoviesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field() # 电影名字
    num = scrapy.Field() # 电影排名
    year = scrapy.Field() # 电影年份
    areas = scrapy.Field() # 电影地区
    styles = scrapy.Field() # 电影类型
