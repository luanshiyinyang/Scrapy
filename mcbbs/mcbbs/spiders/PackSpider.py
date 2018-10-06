import scrapy
from scrapy import Selector
from mcbbs.items import McbbsItem
'''
爬取mcbbs整合包区块的整合包贴名，并且通过xpath或者re（正则表达式）进入相关链接爬取所含主要mod

'''


class PackSpider(scrapy.Spider):
    name = 'mc_pack'

    def __init__(self):
        # 帖子域名
        self.server_link = 'http://www.mcbbs.net'
        self.allowed_domains = ['www.mcbbs.net']
        str1 = 'http://www.mcbbs.net/forum.php?mod=forumdisplay&fid=170&page='
        # 产生前十列的所有链接
        self.start_urls = [(str1 + str(item)) for item in range(2, 51)]

    def start_requests(self):
        for item in self.start_urls:
            yield scrapy.Request(url=item, callback=self.parse1)

    # 解析内容获得每个帖子的地址
    def parse1(self, response):
        hxs = Selector(response)
        items = []
        # 获取链接
        urls = hxs.xpath(r'//a[@onclick="atarget(this)"]/@href').extract()
        # 获取帖子名称
        dir_names = hxs.xpath(r'//a[@onclick="atarget(this)"]/text()').extract()
        for index in range(len(urls)):
            item = McbbsItem()
            item["link_url"] = self.server_link + "/" + urls[index]
            item["dir_name"] = dir_names[index]
            items.append(item)
        # 根据每个帖子链接，发送Request请求，传递item
        for item in items:
            yield scrapy.Request(url=item["link_url"], meta={"item": item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        hxs = Selector(response)
        context = hxs.xpath(r'//tbody/tr[last()-2]/td/text()').extract()
        item["dir_content"] = context
        yield item
