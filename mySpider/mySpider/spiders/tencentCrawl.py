# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from mySpider.items import tencentCrawlItem
import re

class TencentcrawlSpider(CrawlSpider):
    name = "tencentCrawl"
    allowed_domains = ["careers.tencent.com"]
    start_urls = [
        "https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1574936631101&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=2&pageSize=10&language=zh-cn&area=cn"
    ]
    page_lx = LinkExtractor(allow=('start=\d+'))
    rules = [Rule(page_lx, callback='parse_page', follow=True),]
    # ,Rule(LinkExtractor(allow = ('/question/\d+', )), callback = 'parse_page', follow = True),

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "http://careers.tencent.com/position.php?&start=0#a"
    }
    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
    def parse_page(self, response):
        for each in response.xpath('//div[@class="recruit-list"]'):
            item = tencentCrawlItem()
            name = each.xpath('./a/text()').extract()[0]
            detailLink = each.xpath('./div/div/div[3]/@id').extract()[0]
            positionInfo = each.xpath('./a/p[2]').extract()[0]
            peopleNumber = each.xpath('./a/p[1]/span[1]/text()').extract()[0]
            workLocation = each.xpath('./a/p[1]/span[1]/text()').extract()[0]
            publishTime = each.xpath('./a/p[1]/span[5]/text()').extract()[0]

            # print name, detailLink, catalog, peopleNumber, workLocation,publishTime

            item['name'] = name.encode('utf-8')
            item['detailLink'] = detailLink.encode('utf-8')
            item['positionInfo'] = positionInfo.encode('utf-8')
            item['peopleNumber'] = peopleNumber.encode('utf-8')
            item['workLocation'] = workLocation.encode('utf-8')
            item['publishTime'] = publishTime.encode('utf-8')
        #problem = Selector(response)
            # item = tencentCrawlItem()
            # item['url'] = response.url
            # item['name'] = problem.xpath('//span[@class="name"]/text()').extract()
            # print(item['name'])
            # item['title'] = problem.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
            # item['description'] = problem.xpath('//div[@class="zm-editable-content"]/text()').extract()
            # item['answer']= problem.xpath('//div[@class=" zm-editable-content clearfix"]/text()').extract()
        #return item
            curpage = re.search('(\d+)',response.url).group(1)
            page = int(curpage) + 10
            url = re.sub('\d+', str(page), response.url)

            # 发送新的url请求加入待爬队列，并调用回调函数 self.parse
            yield scrapy.Request(url, callback = self.parse)

            # 将获取的数据交给pipeline
            yield item
        #print(response.xpath('//*[@class="correlation-degree"]'))