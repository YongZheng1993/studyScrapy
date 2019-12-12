# -*- coding: utf-8 -*-
import scrapy


class TencentgetSpider(scrapy.Spider):
    name = 'tencentGET'
    allowed_domains = ['tencent.com']
    start_urls = ['http://tencent.com/']


    def parse(self, response):
        pass
