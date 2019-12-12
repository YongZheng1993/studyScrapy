import scrapy

class woshipmCrawlItem(scrapy.Item):
    title = scrapy.Field()#文章标题
    url = scrapy.Field()#文章url
    AricInfo = scrapy.Field()#文章信息
    publishTime = scrapy.Field()#文章发布时间