# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TiantianshuwuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 每一个章节链接
    link_url = scrapy.Field()
    # 每一章的章节名
    dir_name = scrapy.Field()
    # 每一章的内容
    dir_content = scrapy.Field()
    # 每一章内容存放的js文件
    content_js_url = scrapy.Field()
