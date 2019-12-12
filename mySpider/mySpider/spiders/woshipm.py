# -*- coding: utf-8 -*-
import scrapy


class WoshipmSpider(scrapy.Spider):
    name = 'woshipm'
    allowed_domains = ['woshipm.com']
    start_urls = ['http://woshipm.com/']

    def parse(self, response):
        pass
