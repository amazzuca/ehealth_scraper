import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
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
    name = "nosurrender"
    allowed_domains = ["nosurrenderbreastcancersupportforum.com"]
    start_urls = [
        "http://www.nosurrenderbreastcancersupportforum.com/",
    ]

    rules = (
            # Rule to go to the single product pages and run the parsing function
            # Excludes links that end in _W.html or _M.html, because they point to 
            # configuration pages that aren't scrapeable (and are mostly redundant anyway)
            Rule(LinkExtractor(
                    restrict_xpaths='//td[contains(@valign,"top")]/table[contains(@class,"tables")]//a[contains(@class,"forum")]',
                ), callback='internallist'))            
            # Rule to follow arrow to next product grid
            

    # https://github.com/scrapy/dirbot/blob/master/dirbot/spiders/dmoz.py
    # https://github.com/scrapy/dirbot/blob/master/dirbot/pipelines.py
    def internallist(self,response):
           links = response.xpath('id("main_container")/div[2]/form[1]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/a/@href').extract()
           for link in links:
               yield Request(link, callback=self.parsePostList)
            

    def parsePostsList(self,response):
        sel = Selector(response)
        html = response.body
        soup = BeautifulSoup(html)
        users = soup.findAll('a',{'class':re.compile('usergroup\d.*')})
        items = []
        topic = response.xpath('//tbody/tr[2]/td[2]/table/tbody/tr[1]/td/div/b').extract()
        url = response.url
        for x in range(len(users)):
            item = PostItemsList()
            item['author'] = users[x].text
            item['author_link']=users[x]['href']
            item['create_date']= soup.findAll('span',{'id':re.compile('posted_date_.*')})[x].text
            item['post'] = soup.findAll('span',{'id':re.compile('post_message.*')})[x].text
            item['tag']='cancer'
            item['topic'] = topic
            item['url']=url
            logging.info(item.__str__)
            items.append(item)
        return items
