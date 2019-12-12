# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.htmls
import json
#from scrapy.conf import settings
from mySpider.settings import MONGODB_HOST
from mySpider.settings import MONGODB_PORT
from mySpider.settings import MONGODB_DBNAME
from mySpider.settings import MONGODB_DOCNAME
from mySpider.settings import MONGODB_USER
from mySpider.settings import MONGODB_PSW
import pymongo

class  woshipmJsonPipeline(object):
    def __init__(self):
        # 可选实现，做参数初始化等
        # doing something
        self.file = open('woshipm.json', 'w')
        # 获取setting主机名、端口号和数据库名
        host = MONGODB_HOST
        port = MONGODB_PORT
        dbname = MONGODB_DBNAME

        # pymongo.MongoClient(host, port) 创建MongoDB链接
        #client = pymongo.MongoClient(host=host,port=port)
        # 定义数据库链接
        client = pymongo.MongoClient(
            'mongodb://{0}:{1}@{2}:{3}'.format(MONGODB_USER, MONGODB_PSW,MONGODB_HOST,
                                               MONGODB_PORT))
        #self.db = self.client[settings.MONGO_DB]  # 获得数据库的句柄
        #self.coll = self.db[settings.MONGO_COLL]  # 获得collection的句柄
        # 指向指定的数据库
        mdb = client[dbname]
        # 获取数据库里存放数据的表名
        self.post = mdb[MONGODB_DOCNAME]

    def process_item(self, item, spider):
        # item (Item 对象) – 被爬取的item
        # spider (Spider 对象) – 爬取该item的spider
        # 这个方法必须实现，每个item pipeline组件都需要调用该方法，
        # 这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理。
        #return item
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(content)# 写到文件json
        self.post.insert(dict(item))#写到mongoDB
        return item


