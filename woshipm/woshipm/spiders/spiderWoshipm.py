# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import json
import urllib
from  woshipm.items  import  WoshipmItem
from datetime import datetime
# 百度api 获取摘要
from aip import AipNlp
import time

class SpiderwoshipmSpider(scrapy.Spider):
    name = 'spiderWoshipm'
    #start_urls = ['http://woshipm.com/']
    #定义外部关键词
    keywordList = []# ['互联网金融','产品设计']
    #爬虫开始网址
    start_urls = []  # ['https://36kr.com/search/articles/OYO',]
    #传入Url的关键词
    keyword=''
    # 搜索页面最后请求访问url
    url = 'https://4ocsfs3sim-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.21.1%3Binstantsearch.js%201.11.7%3BJS%20Helper%202.19.0&x-algolia-application-id=4OCSFS3SIM&x-algolia-api-key=7bd75daaf81d0299565fce2232394dfd'
    # 请求header
    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Cookie': 'Hm_lvt_de6470f7123b10c2a7885a20733e9cb1=1573008943,1573265635; _nbd_session_id=30b02d48f265fb61147180e26f06bac1; Hm_lpvt_de6470f7123b10c2a7885a20733e9cb1=1573265678',
        'Content-Type': 'application/json'
    }
    # urlList.append(self.url + parse.quote(keyword))
    # 默认 显示 页面1 得到所有 查询新闻结果页面
    #
    #url = 'https://36kr.com/search/articles/'
    #定义外部传入参数  start_urls 爬虫网址  keywordList 关键词
    def __init__(self, start_urls='', keywordList='', *args, **kwargs):
        super(SpiderwoshipmSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_urls]
        self.keywordList = [keywordList]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
        # fp = open( log_file_path, 'w')  # 如果有这个文件就打开，如果没有这个文件就创建一个名叫CSDN的txt文件
        # self.logger.info('Parse function called on %s', response.url)

        headers = {
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Content-Type': 'application/json',

        }

        urlList = []
        #keyword = ''
        for key in self.keywordList:
            self.keyword = key
            # 中文转 网页编码 parse.quote(keyword)
            # start_urls.append(url+parse.quote(keyword))
            # print()
            query = {'k': '{}'.format(self.keyword), 'is_v': 1}
            self.headers['Referer'] = 'http://www.woshipm.com/search-posts?' + urllib.parse.urlencode(query)
            print(self.headers['Referer'])
            # print('keywordList: ',self.keywordList)
            data = json.dumps({"requests": [{"indexName": "w_searchable_posts",
                                             "params": "query={}&hitsPerPage=20&page=0&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&facetingAfterDistinct=true&facets=%5B%5D&tagFilters=".format(
                                                 parse.quote(self.keyword))}]})
            print('data', data)

            yield scrapy.Request(self.url,
                                 method='POST',
                                 headers=headers, body=json.dumps({"requests": [{"indexName": "w_searchable_posts",
                                                                                 "params": "query=xxx&hitsPerPage=20&page=0&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&facetingAfterDistinct=true&facets=%5B%5D&tagFilters="}]}),
                                 callback=self.parse_page)

    def parse_page(self, response):
        #print('response:', response.text)
        #print(json.loads(response.text)['results'])
        #print(type(json.loads(response.text)['results'][0]))
        responseDict = json.loads(response.text)['results'][0]
        print(responseDict['nbHits'])
        totalPage = int(responseDict['nbHits'])//20
        print(totalPage)
        for i in range(0,totalPage+2):
            print(i)
            body=json.dumps({"requests": [{"indexName": "w_searchable_posts",
                                             "params": "query={}&hitsPerPage=20&page={}&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&facetingAfterDistinct=true&facets=%5B%5D&tagFilters=".format(
                                                 parse.quote(self.keyword),i)}]})
            #print(body)
            yield scrapy.Request(self.url,
                                 method='POST',
                                 headers=self.headers, body=body,
                                 callback=self.parse_getAricInfo)
    #循环每页得到
    def parse_getAricInfo(self,response):
        responseDict = json.loads(response.text)['results'][0]
        print(type(responseDict['hits']),'-----')
        for aricInfoDict in responseDict['hits']:
            item = WoshipmItem()
            #取文章Url
            item['url'] = 'http://www.woshipm.com/copy/'+str(aricInfoDict['post_id'])+'.html'
            #取当前时间
            item['createTime'] = str(datetime.now())
            item['publishTime'] = aricInfoDict['post_date']
            item['author'] = aricInfoDict['post_author']['display_name']
            item['title']= aricInfoDict['post_title']
            # 获取文章的整个网页以及 调用百度摘要
            yield scrapy.Request(
                url=item['url'],
                callback=self.parse_getAricDetailInfo,
                meta = {'item':item}
                )
            # 获取文章的整个网页以及 调用百度摘要
    def parse_getAricDetailInfo(self,response):
            #items = []
            # 通过meta 传递参数
            item = response.meta["item"]
            # 获取到文章内容
            item['content'] = response.xpath("//div[@class ='grap']//p/text()").extract()
            # 文章 题目
            options = {}
            content = {}
            # 调用 百度API ai借口
            itemTemp =item['content'][0]
            content['content'] = itemTemp[1:2000].replace('\xa0', '')
            options['title'] = item['title'][0]
            """ 你的 APPID AK SK """
            APP_ID = '15581558'
            API_KEY = '8Wooot48PG5Qkd91MC3KPbPZ'
            SECRET_KEY = '5m25xH393bejzo6HG9SKtfb44anEPsFL'
            # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            #生成 链接
            client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
            # 读取数据
            # articles = pd.read_excel('百度AI接口调用文章示例.xlsx')
            # 获取摘要
            maxSummaryLen = 150
            try:
                # print(options,content)
                #获取摘要 百度介绍地址 https://ai.baidu.com/docs#/NLP-Python-SDK/87e2d0c5
                summary = client.newsSummary(content['content'], maxSummaryLen, options)['summary']
                #item['summary']=summary
                print('找到摘要')
                errorSummary = ''
                time.sleep(1)
            except:
                summary = ''
                # 记录整个调用返回结果
                errorSummary = client.newsSummary(content['content'], maxSummaryLen, options)
            item['summary'] = summary
            item['errorSummary'] = errorSummary
            try:
                #获取标签
                itemsTag = client.keyword(options['title'], content['content'])['items']
                tags = '、'.join([itemTag['tag'] for itemTag in itemsTag])
                time.sleep(1)
                errorTags = ''
                print('找到标签')
            except:
                #print()
                errorTags = client.keyword(options['title'], content['content'])
                tags = ''
            item['tags'] = tags
            item['errorTags'] = errorTags

            yield item








