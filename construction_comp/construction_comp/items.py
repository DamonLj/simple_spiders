# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ConstructionCompItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    adress = scrapy.Field()
    # id = scrapy.Field()
    lrperson = scrapy.Field()
    certifications = scrapy.Field()
