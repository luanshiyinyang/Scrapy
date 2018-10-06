# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from mcbbs import settings


class McbbsPipeline(object):
    def process_item(self, item, spider):

        with open(settings.STORE, 'a') as f:
            f.write(item['dir_name']+"    :     ")
            f.write(str(item['dir_content'])+"\n")
        return item
