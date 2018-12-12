# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    # 第一种方式
    # start_urls = ['https://hr.tencent.com/position.php?&start={}'.format(page*10) for page in range(1,282)]

    # 第二种方式
    baseURL = 'https://hr.tencent.com/position.php?&start='
    offset = 0
    start_urls = [baseURL + str(offset)]

    def parse(self, response):
        print(response)

        list = response.xpath('//tr[@class="even"] | //tr[@class="odd"]')
        for node in list:
            name = node.xpath('./td[1]/a/text()').extract()[0].encode('utf-8')
            link = node.xpath('./td[1]/a/@href').extract()[0].encode('utf-8')
            if node.xpath('./td[2]/text()'):
                type = node.xpath('./td[2]/text()').extract()[0].encode('utf-8')
            else:
                type = ""

            number = node.xpath('./td[3]/text()').extract()[0].encode('utf-8')
            location = node.xpath('./td[4]/text()').extract()[0].encode('utf-8')
            time = node.xpath('./td[5]/text()').extract()[0].encode('utf-8')

            item = TencentItem()
            item['name'] = name
            item['link'] = link
            item['type'] = type
            item['number'] = number
            item['location'] = location
            item['time'] = time
            yield item

        # 第二种方式 判断是不是最后一页 拼接地址
        # if self.offset < 2190:
        #     self.offset += 10
        #     url = self.baseURL + str(self.offset)
        #     print(url)
        #     yield scrapy.Request(url,callback=self.parse)

        # 第二种方式的优化方式  两种方式中 最好的方式
        # 动态获取是否有请求地址 有的化获取下一页面 找到next
        if len(response.xpath('//a[@class="noactive" and @id="next"]')) == 0:
            url = response.xpath('//a[@id="next"]/@href').extract()[0]
            yield scrapy.Request("https://hr.tencent.com/" + url,callback=self.parse)
