from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class PaperSpider(BaseSpider):
    name = "paper"
    allowed_domains = ["epa.gov.tw"]
    start_urls = [
	"http://eiareport.epa.gov.tw/EIAWEB/00.aspx"
    ]

    def parse(self,response):
	filename = "00"
        selector = HtmlXPathSelector(response)
        pages = selector.select("//a[contains(@href,'gvAbstract')]/text()").extract()
        filename = 'page_count'
        open(filename, 'wb').write(','.join(pages))

