mySpider/                   /*创建scrapy工程 mySpider 为项目名称*/
├── __init__.py 
├── log                    /*创建scrapy工程 mySpider项目日志文件夹，第一次需要人工创建log文件夹*/ 
├── mySpider
│   ├── __init__.py
│   ├── items.py            /*项目默认的目标文件，定义输出结果字段*/
│   ├── middlewares.py      /*项目默认的中间件设置*/
│   ├── pipelines.py        /*项目默认的管道文件 */ 
│   ├── settings.py         /*项目默认的设置文件 ,例如数据库配置 */ 
│   ├── spiders
│   │   ├── __init__.py
│   │   ├── itcast.py       /*项目的爬虫文件，默认爬虫名与文件名一样-- scrapy genspider itcast "itcast.cn"*/  
│   │   ├── renren.py       
│   ├── woshipmItems.py     /*自己根据爬虫网站不一样，新建目标文件*/
│   └── woshipmPipelines.py /*自己根据爬虫网站不一样，新建管道文件*/
├── scrapy.cfg
├── readme.md
