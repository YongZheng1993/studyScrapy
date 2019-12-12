# -*- coding: utf-8 -*-
import scrapy

from mySpider.items import TencentItem
import  json
import re
import time

class TencentSpider(scrapy.Spider):
    #name = 'tencent'
    #allowed_domains = ['tencent.com']
    #start_urls = ['http://tencent.com/']
    name = "tencent"
    allowed_domains = ["careers.tencent.com"]
    start_urls = [
        "https://careers.tencent.com/tencentcareer/api/post/Query?countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn"
    ]
    #def parse(self, response):
    #    pass
    def parse(self, response):
        time.sleep(2)
        #rs = response.json()['data']
        jsonData = json.loads(response.text)['Data']
        PostsListData=jsonData['Posts']
        #print(PostsData[0])
        item = TencentItem()
        if PostsListData is not None:
            curpage = re.search('(\d+)', response.url).group()
            page = int(curpage) + 1
            url = re.sub('\d+', str(page), response.url,1)
            PostsDictData = PostsListData[0]

            # {}
            name = PostsDictData['RecruitPostName']
            detailLink = PostsDictData['PostURL']
            positionInfo = PostsDictData['Responsibility']
            peopleNumber = '2'
            workLocation = PostsDictData['CountryName'] + ',' + PostsDictData['LocationName']
            publishTime = PostsDictData['LastUpdateTime']
            item['name'] = name
            item['detailLink'] = detailLink
            item['positionInfo'] = positionInfo
            item['peopleNumber'] = peopleNumber
            item['workLocation'] = workLocation
            item['publishTime'] = publishTime
            #print(page,url)
            yield scrapy.Request(url, callback=self.parse)
        else:
            print(re.search('(\d+)', response.url).group(),response.url)
            print('所有跑完----')
        #print(json.loads(response.text)['Data'])

        #curpage = re.search('(\d+)',response.url).group()
        #page = int(curpage) + 1
        #url = re.sub('\d+', str(page), response.url)
        # 发送新的url请求加入待爬队列，并调用回调函数 self.parse
        #yield scrapy.Request(url, callback=self.parse)
        #
        # for each in response.xpath('//div[@class="search-content"]'):
        #     item = TencentItem()
        #     name = each.xpath('./div/div/a/text()').extract()[0]
        #     detailLink = each.xpath('./td[1]/a/@href').extract()[0]
        #     positionInfo = each.xpath('./td[2]/text()').extract()[0]
        #     peopleNumber = each.xpath('./td[3]/text()').extract()[0]
        #     workLocation = each.xpath('./td[4]/text()').extract()[0]
        #     publishTime = each.xpath('./td[5]/text()').extract()[0]
        #
        #
        #     #print name, detailLink, catalog, peopleNumber, workLocation,publishTime
        #
        #     item['name'] = name.encode('utf-8')
        #     item['detailLink'] = detailLink.encode('utf-8')
        #     item['positionInfo'] = positionInfo.encode('utf-8')
        #     item['peopleNumber'] = peopleNumber.encode('utf-8')
        #     item['workLocation'] = workLocation.encode('utf-8')
        #     item['publishTime'] = publishTime.encode('utf-8')
        #
        #     curpage = re.search('(\d+)',response.url).group(1)
        #     page = int(curpage) + 10
        #     url = re.sub('\d+', str(page), response.url)
        #
        #     # 发送新的url请求加入待爬队列，并调用回调函数 self.parse
        #     yield scrapy.Request(url, callback = self.parse)
        #
        #     # 将获取的数据交给pipeline
        yield item
        # print(response.xpath('//*[@class="correlation-degree"]'))