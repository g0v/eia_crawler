from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

class DetailSpider(Spider):
    name = 'detail'
    allowed_domains = ["epa.gov.tw"]

    def __init__(self, hcode=None, *args, **kwargs):
        super(DetailSpider,self).__init__(*args,**kwargs)
        hcode = '1030536A'

        self.start_urls =[
            "http://eiareport.epa.gov.tw/EIAWEB/10.aspx?hcode=%s" % (hcode)
        ]

        pass

    def parse(self,response):
        print response.body

        # go to the detail page
        yield Request("http://eiareport.epa.gov.tw/EIAWEB/10_0.aspx",callback=self.parse_detail)

        pass

    def parse_detail(self,response):
        print response.body

        pass

    pass


