# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tiantianshuwu import settings
import os
class TiantianshuwuPipeline(object):
    def process_item(self, item, spider):
        # 检查存放目录是否存在，不存在则创建目录
        if os.path.exists(settings.STORE):
            pass
        else:
            os.makedirs(settings.STORE)
        # 每一章内容以txt文件写入文件夹
        with open(settings.STORE+'\\'+item['dir_name'].strip()+".txt", 'w') as f:
            f.write(item['dir_content'])
        return item
