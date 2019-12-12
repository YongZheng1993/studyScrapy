# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib import parse
import json
import urllib
from mySpider.woshipmItems import woshipmCrawlItem
from mySpider.settings import log_file_path
import time, os, logging

#item = ItcastItem()
from requests.cookies import RequestsCookieJar
from scrapy.http.cookies import CookieJar    # 该模块继承自内置的http.cookiejar,操作类似
import re

class WoshipmcrawlSpider(CrawlSpider):
    name = 'woshipmCrawl'
    #allowed_domains = ['woshipm.com']
    keywordList = []# ['互联网金融','产品设计']
    start_urls= []#['https://36kr.com/search/articles/OYO',]

    url = 'https://36kr.com/search/articles/'

    def __init__(self, start_urls='', keywordList='', *args, **kwargs):
        super(WoshipmcrawlSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_urls]
        self.keywordList = [keywordList]



    def getwoshipmCookie(self,cookies,lenCookies):
        #获取 登陆时 36氪 的cooike
        cookiesList={}
        #cookies =response.headers.getlist('Set-Cookie')
        #print(cookies,'----')
        for x in range(0,lenCookies):
            each = str(cookies[x])
            # print(each,each.split(";"))
            i = str(each.split(";")[0]).replace('b\'', '')
            cookiesList[i.split("=")[0]] = i.split("=")[1]
        return cookiesList

    #先登陆 36氪 获取cookie
    def parse(self, response):
        #fp = open( log_file_path, 'w')  # 如果有这个文件就打开，如果没有这个文件就创建一个名叫CSDN的txt文件
        self.logger.info('Parse function called on %s', response.url)

        #logging.WARNING('111')
        #my_logger = self.get_logger(str(time.strftime('%Y%m%d%H%M%S', time.localtime())))
        #my_logger.info('Info logger')

        #my_logger.warning('Warning logger')

        #my_logger.error('Error logger')
        #print(response.headers.getlist('Cookie'))

        headers = {
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Content-Type': 'application/json',

        }
        cookiesList = {}
        #获取 登陆时 36氪 的cooike
        cookies =response.headers.getlist('Set-Cookie')
        #print(cookies,'----')
        lenCookies = len(response.headers.getlist('Set-Cookie'))
        # 默认传入 self
        cookiesList = self.getwoshipmCookie(cookies,lenCookies)
        #获取总条数
        urlList=[]
        print('keywordList: ',self.keywordList)
        #totalCount=response.xpath('//div[@class="total-count"]').extract()
        for keyword in self.keywordList:
            # 中文转 网页编码 parse.quote(keyword)
            # start_urls.append(url+parse.quote(keyword))
            print()
            urlList.append(self.url + parse.quote(keyword))

        #print(urlList)
        #print(cookiesList)
        for startUrl in urlList:
            headers['Referer']= startUrl
            yield scrapy.Request(startUrl,headers = headers,cookies= cookiesList,callback=self.parse_page)
        #fp.close()

        #self.logger.info('Parse function called on %s', response.url)
        #return cookiesList
    #"entity_type": "post","keyword": "OYO","page": 2,"per_page": 40,"sort": "date"
    #return cookiesList
    # 获取 输入关键词的页面的查询结果
    def parse_page(self, response):
        headers = {
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Content-Type': 'application/json',

        }

        cookiesList = {}
        #print(response.text)
        cookies =response.headers.getlist('Set-Cookie')
        lenCookies = len(response.headers.getlist('Set-Cookie'))
        cookiesList = self.getwoshipmCookie(cookies,lenCookies)
        print('cookies:',cookies,'cookiesList:',cookiesList)
        print(response.xpath('//div[@class="total-count"]/text()').extract())
        totalCount = response.xpath('//div[@class="total-count"]/text()').extract()[3]
        #print(totalCount)
        #获取 登陆时 36氪 的cooike
        refeferUrl = response.url
        print(refeferUrl,'-----')
        headers['Referer'] = refeferUrl
        bodyKeyword = urllib.parse.unquote(refeferUrl.split("/")[-1])
        # 网页编码转中文
        #print(urllib.parse.unquote(bodyKeyword))
        #headers['sec-fetch-mode'] = 'cors'
        #headers['sec-fetch-site'] = 'same-origin'
        headers['m-x-xsrf-token'] = cookiesList['M-XSRF-TOKEN']
        #body = json.dumps({'entity_type': "post","keyword": "{}".format(bodyKeyword),"page": '2',"per_page": '40',"sort": "date"})
        #item = TencentItem()
        #print(response.text,response.headers.getlist('Cookie'))
        #print(response.headers) #)['data'])
        #print(json.loads(response.text))#['data']['total_count'])
        rangePage = int(totalCount)//40 +1
        for i in range(1,2):
            yield scrapy.Request(
                url='https://36kr.com/pp/api/search/entity-search',
                headers = headers,
                body = json.dumps({'entity_type': "post","keyword": "{}".format(bodyKeyword),"page": '{}'.format(i),"per_page": '40',"sort": "date"}),
                method = 'POST',
                #meta={},
                cookies= cookiesList,
                callback=self.parse_detailPage
                #errback=self.error,  # 本项目中这里触发errback占绝大多数
                #dont_filter=True,  # 按理来说是不需要加此参数的
            )


    def parse_detailPage(self, response):
        #items = []
        for i in json.loads(response.text)['data']['items']:
            #print(type(i),i['id'],i['title'],i['template_info'])
            item = woshipmCrawlItem()
            #publishTime
            item['title']=i['title']
            item['url'] ='https://36kr.com/p/'+str(i['id'])
            item['AricInfo'] = '1'
            item['publishTime'] = i['published_at']

            yield scrapy.Request(
                url=item['url'],
                callback=self.parse_getAric,
                meta = {'item':item}
                )
            #print(response1)
            #print(item)

                #headers=headers,
            #url = scrapy.Field()
            #AricInfo = scrapy.Field()

            # peopleNumber = scrapy.Field()
            # workLocation = scrapy.Field()
            #= scrapy.Field()

    def parse_getAric(self, response):
        items = []
        #AricInfo = response.xpath("//div[@class='article-mian-content']/text()").extract()
        print(response.meta["item"])
        item = response.meta["item"]
        #print('---',AricInfo)
        item['AricInfo'] = response.xpath("//div[@class ='article-mian-content']/div/div[2]/div/p/text()").extract()
        #return AricInfo
        ##common-width margin-bottom-20
        items.append(item)
        print(items)
        return items

        #class ="common-width margin-bottom-20"



