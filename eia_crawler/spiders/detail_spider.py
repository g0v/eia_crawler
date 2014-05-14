import csv
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from urlparse import urlparse,parse_qs

make_input_pattern_string = lambda id: "//input[contains(@id,'%s')]/@value" % (id)
make_span_pattern_string = lambda id: "//span[contains(@id,'%s')]/text()" % (id)

class DetailSpider(Spider):
    LIST_FOLDER = 'results/list'
    DETAIL_FOLDER = 'results/detail'

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

    def __init__(self, *args, **kwargs):
        super(DetailSpider,self).__init__(*args,**kwargs)

        # read the hcode from the list/result.csv file and generate all start_urls
        self.start_urls = [];

        with open("%s/%s" % (self.LIST_FOLDER,'result.csv')) as f:
            reader = csv.DictReader(f)
                  
            for row in reader:
                hcode = row['HCODE']
                url = "http://eiareport.epa.gov.tw/EIAWEB/10.aspx?hcode=%s" % (hcode)
                self.start_urls.append(url)

        self.fout = open('%s/%s.csv' % (self.DETAIL_FOLDER,'result'),'wb')
        header = ['HCODE'] + self.patterns.keys()
        self.writer = csv.DictWriter(self.fout,header)
        self.writer.writeheader()

        pass

    def __del__(self):
        super(DetailSpider,self).__del()

        self.fout.close()
        pass

    def parse(self,response):
        query_string = urlparse(response.url).query
        hcode = parse_qs(query_string)['hcode'][0]

        # go to the detail page
        yield Request("http://eiareport.epa.gov.tw/EIAWEB/10_0.aspx",
                        meta={'HCODE': hcode},
                        callback=self.parse_detail,dont_filter=True)

        pass

    def parse_detail(self,response):    
        # get the attribute of field
        def getAttr(selector,pattern):
            result = selector.xpath(pattern).extract()
            return result[0].encode('utf8') if (len(result)>0) else ''

        Sel = Selector(response)

        item = {}
        
        hcode = response.meta['HCODE']   
        item['HCODE'] = hcode

        for attr,pattern in self.patterns.iteritems():
            item[attr] = getAttr(Sel,pattern)
        
        self.writer.writerow(item)
        pass

    pass


