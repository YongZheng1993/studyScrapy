# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WoshipmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #定义 输出字段列
    title = scrapy.Field() #  标题
    createTime = scrapy.Field() # 创建时间
    publishTime = scrapy.Field() # 文章发布时间
    summary = scrapy.Field() #摘要
    tags = scrapy.Field() #标签
    url = scrapy.Field() #文章 url
    content = scrapy.Field() # 文章内容
    author = scrapy.Field() # 文章作者
    errorSummary = scrapy.Field() #未找到摘要报错
    errorTags = scrapy.Field()  #未找到标签报错

    pass
