import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from forum.items import PostItemsList
import re
import logging
from bs4 import BeautifulSoup

## LOGGING to file
#import logging
#from scrapy.log import ScrapyFileLogObserver

#logfile = open('testlog.log', 'w')
#log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
#log_observer.start()

# Spider for crawling Adidas website for shoes
class ForumsSpider(CrawlSpider):
    name = "epilepsy_ehealthforums_spider"
    allowed_domains = ["cancerresearch.org"]
    start_urls = [
        "https://www.cancerresearchuk.org/about-cancer/cancer-chat/",
    ]

    rules = (
            # Rule to go to the single product pages and run the parsing function
            # Excludes links that end in _W.html or _M.html, because they point to 
            # configuration pages that aren't scrapeable (and are mostly redundant anyway)
            Rule(LinkExtractor(
                    restrict_xpaths='//div[contains(@class,"table-list views-table cols-5")]/ol/li/div[1]/a[1]',
                ), callback='parsePostsList'),
            # Rule to follow arrow to next product grid
            Rule(LinkExtractor(
                    restrict_xpaths='//li[@class="next last"]',
                ), follow=True),
        )

    # https://github.com/scrapy/dirbot/blob/master/dirbot/spiders/dmoz.py
    # https://github.com/scrapy/dirbot/blob/master/dirbot/pipelines.py
    def parsePostsList(self,response):
        sel = Selector(response)
        html = response.body
        soup = BeautifulSoup(html.read())
        users = soup.findAll('a',{'class':'username'})
        items = []
        topic = response.xpath('//h1/text()').extract()
        url = response.url
        for x in range(len(users)):
            item = PostItemsList()
            item['author'] = soup.findAll('a',{'class':'username'})[x].text
            item['author_link']=soup.findAll('a',{'class':'username'})[x]['href']
            item['create_date']= soup.findAll('div',{'class':'post-content-inner'})[x].span.text[0:10]
            item['post'] = soup.findAll('div',{'class':'post-content-inner'})[x].find('div',{'class':'field-item even'}).text
            item['tag']='cancer'
            item['topic'] = topic
            item['url']=url
            logging.info(item.__str__)
            items.append(item)
        return items
