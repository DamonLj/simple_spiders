# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from collections import OrderedDict


class TopmoviesPipeline(object):
    def process_item(self, item, spider):
        return item


class Topmovies2txtPipeline(object):
    def open_spider(self, spider):
        self.f = open('topMovies.txt', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        try:
            line = str(dict(item)) + '\n'
            self.f.write(line)
        except:
            pass
        return item


class Topmovies2jsonPipeline(object):
    def open_spider(self, spider):
        self.f = codecs.open('topMovies.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        try:
            line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + '\n'
            self.f.write(line)
        except:
            pass
        return item

