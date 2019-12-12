# -*- coding: utf-8 -*-
import scrapy
import re


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/518558772/profile']
#重写 reques 函数
    def start_requests(self):
        cookies = 'anonymid=k3nsaesv6oy8b8; depovince=SH; jebecookies=0ec43bec-b537-45f3-9d97-c0416ab70af9|||||; _r01_=1; JSESSIONID=abc8VQ4yzfses5Ld-ue7w; ick_login=e2ed1c83-477c-4a81-b9e8-e1b7060e313a; _de=A2D1178C875FD07980CE3A606DDE588E6DEBB8C2103DE356; p=9ae7bb6774936482e7ac6317bd1378f42; first_login_flag=1; ln_uact=p01114245@126.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn421/20130407/1745/h_main_OhmS_a1f5000001f3113e.jpg; t=102986f7ab57f4d8e0f89e0c7a8ef99a2; societyguester=102986f7ab57f4d8e0f89e0c7a8ef99a2; id=518558772; xnsid=3babea1f; ver=7.0; loginfrom=null; jebe_key=807decb8-5fe2-424e-80c3-e9fd2b6fad9c%7C754ca0019477fc01c4e4eb788b3e96b0%7C1575251876998%7C1%7C1575251701043; wp_fold=0'
        #需要字典类型数据
        cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split("; ")}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            cookies = cookies
        )
    def parse(self, response):
        print(re.findall('郑勇',response.body.decode()))
