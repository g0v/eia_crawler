from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

make_input_pattern_string = lambda id: "//input[contains(@id,'%s')]/@value" % (id)
make_span_pattern_string = lambda id: "//span[contains(@id,'%s')]/text()" % (id)

class DetailSpider(Spider):
    name = 'detail'
    allowed_domains = ["epa.gov.tw"]

    patterns = {
        'DOCTYP': make_span_pattern_string('lbDOCTYP'),
        'DEPN': make_input_pattern_string('txDEPN'),
        'DST': make_input_pattern_string('txDST'),
        'DECAL': make_input_pattern_string('txDECAL'),
        'DAREA': make_input_pattern_string('txDAREA'),
        'DSIZE': make_input_pattern_string('txDSIZE'),
        'DSUNT': make_input_pattern_string('txDSUNT'),
        'TAKER': make_input_pattern_string('txTAKER'),
        'DIRORG': make_input_pattern_string('txDIRORG'),
        'SEDAT': make_input_pattern_string('txSEDAT'),
        'PORCS': make_input_pattern_string('txPORCS'),
        'TRIA': make_input_pattern_string('txTRIA'),
        'EXTP': make_input_pattern_string('txEXTP'),
        'COMIT': make_input_pattern_string('txCOMIT'),
        'NOTES': make_input_pattern_string('txNOTES')
    }

    def __init__(self, hcode=None, *args, **kwargs):
        super(DetailSpider,self).__init__(*args,**kwargs)
        hcode = '1030536A' # Fake hcode

        self.start_urls =[
            "http://eiareport.epa.gov.tw/EIAWEB/10.aspx?hcode=%s" % (hcode)
        ]

        pass

    def parse(self,response):
        # print response.body

        # go to the detail page
        yield Request("http://eiareport.epa.gov.tw/EIAWEB/10_0.aspx",
                    callback=self.parse_detail)

        pass

    def parse_detail(self,response):
        # print response.body
        
        def getAttr(selector,pattern):
            result = selector.xpath(pattern).extract()
            return result[0].encode('utf8') if (len(result)>0) else ''

        Sel = Selector(response)

        item = {}
        for attr,pattern in self.patterns.iteritems():
            item[attr] = getAttr(Sel,pattern)
            print attr,item[attr]

        pass

    pass


