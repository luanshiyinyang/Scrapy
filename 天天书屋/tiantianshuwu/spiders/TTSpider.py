import scrapy
from tiantianshuwu.items import TiantianshuwuItem


class TTSpider(scrapy.Spider):
    name = "tianshu"

    def __init__(self):
        # 链接头
        self.server_link = 'http://www.ttshu.com'
        # 限制域名
        self.allowed_domains = ['www.ttshu.com']
        # 其实http文件
        self.start_url = "http://www.ttshu.com/html/content/18424482.html"

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse1)

    # 解析出每一个章节链接
    def parse1(self, response):
        items = []
        # 查询到存放章节链接的a标签，获得href链接组成列表，该列表存放的就是每一章的链接尾巴
        chapter_urls = response.xpath(r'//td[@bgcolor="#F6F6F6"]/a/@href').extract()
        # 遍历每一个链接放入item
        for index in range(len(chapter_urls)):
            item = TiantianshuwuItem()
            item["link_url"] = self.server_link + chapter_urls[index]
            items.append(item)
        # 对每个链接发出request
        for item in items:
            yield scrapy.Request(url=item['link_url'], meta={"data": item}, callback=self.parse2)

    def parse2(self, response):
        # 获得item对象数据
        item = response.meta['data']
        # 提取h1标签中的章节名称
        item['dir_name'] = response.xpath(r'//h1/text()').extract()[0]
        # 提取js代码链接位置
        item['content_js_url'] = self.server_link + response.xpath(r'//p/script/@src').extract()[0]
        # 请求js文件
        yield scrapy.Request(url=item['content_js_url'], meta={"data": item}, callback=self.parse3)

# 解析js文件解码后的字符串，去掉html文件的符号代替符
    def solve_text(self, content):
        content = content.replace("document.write('", "")
        content = content.replace("' ;", "")
        content = content.replace(")", " ")
        content = content.replace("</br>", "\n")
        content = content.replace("<br />", "\n")
        content = content.replace("<br><br>", "\n")
        content = content.replace("&nbsp;", " ")
        return content

    def parse3(self, response):
        item = response.meta["data"]
        # 解析文档整体，获得文本内容
        item['dir_content'] = self.solve_text(str(response.body.decode('gb2312', 'ignore')))
        yield item









