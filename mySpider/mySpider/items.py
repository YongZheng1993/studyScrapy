# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy.item import Item, Field
#import woshipmItems


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
# 定义管道接收字段类型
class ItcastItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()
#定义爬虫腾讯新闻网 定义输出字段
class TencentItem(scrapy.Item):
    name = scrapy.Field()
    detailLink = scrapy.Field()
    positionInfo = scrapy.Field()
    peopleNumber = scrapy.Field()
    workLocation = scrapy.Field()
    publishTime = scrapy.Field()


class tencentCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # url = scrapy.Field()  #保存抓取问题的url
    # title = scrapy.Field()  #抓取问题的标题
    # description = scrapy.Field()  #抓取问题的描述
    # answer = scrapy.Field()  #抓取问题的答案
    # name = scrapy.Field()  #个人用户的名称
    name = scrapy.Field()
    detailLink = scrapy.Field()
    positionInfo = scrapy.Field()
    peopleNumber = scrapy.Field()
    workLocation = scrapy.Field()
    publishTime = scrapy.Field()