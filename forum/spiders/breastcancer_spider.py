import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from forum.items import PostItemsList
import re
import logging

## LOGGING to file
#import logging
#from scrapy.log import ScrapyFileLogObserver

#logfile = open('testlog.log', 'w')
#log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
#log_observer.start()

# Spider for crawling Adidas website for shoes
class ForumsSpider(CrawlSpider):
    name = "breastcancer_spider"
    allowed_domains = ["http://patient.info/forums/discuss/"]
    start_urls = [
        "http://patient.info/forums/discuss/browse/breast-cancer-and-screening-275",
    ]

    rules = (
            # Rule to go to the single product pages and run the parsing function
            # Excludes links that end in _W.html or _M.html, because they point to 
            # configuration pages that aren't scrapeable (and are mostly redundant anyway)
            Rule(LinkExtractor(
                restrict_xpaths='//h3/a',
                deny=(r'user?returnUrl')), callback='parsePostsList'),
            # Rule to follow arrow to next product grid
            Rule(LinkExtractor(restrict_xpaths="id('group-discussions')/form[1]/a",
            ), follow=True),
        )

    # https://github.com/scrapy/dirbot/blob/master/dirbot/spiders/dmoz.py
    # https://github.com/scrapy/dirbot/blob/master/dirbot/pipelines.py
    def parsePostsList(self,response):
        sel = Selector(response)
        posts = sel.xpath('//div[contains(@class,"disc-forums disc-thread")]')
        items = []
        topic = response.xpath("id('topic')/article/h1/text()").extract()
        url = response.url
        for post in posts:
            item = PostItemsList()
            item['author'] = post.xpath('//div/div/a/p/strong[2]/text()').extract()
            item['author_link']=post.xpath('//div/div/a/@href').re('/forums/profiles.*')
            item['create_date']= post.xpath('//span[contains(@class,"post-meta")]/time/@datetime')[0].extract()
            item['post'] = post.xpath('//div[contains(@class,"post-content break-word")]/p[1]/text()').extract()
            item['tag']='Breast Cancer and Screening'
            item['topic'] = topic
            item['url']=url
            logging.info(item.__str__)
            items.append(item)
        return items

