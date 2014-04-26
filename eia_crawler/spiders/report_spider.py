import csv
from time import time
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest
from eia_crawler.items import ReportSummaryItem

class ReportSpider(Spider):
    LIST_FOLDER = 'results/list'

    name = "report"
    allowed_domains = ["epa.gov.tw"]
    start_urls = [
        "http://eiareport.epa.gov.tw/EIAWEB/00.aspx"
    ]
    last_page_num = -1

    patterns = {
            'HCODE': "td/span[contains(@id,'HCODE')]/text()",
            'DST': "td/span[contains(@id,'DST')]/text()",
            'EDN':"td/span[contains(@id,'EDN')]/@title",
            'DOCTYPE': "td/span[contains(@id,'DOCTYPE')]/text()",
            'PER': "td[6]/text()",
            'EXTP': "td/span[contains(@id,'EXTP')]/text()",
            'NOTES': "td/span[contains(@id,'NOTES')]/@title"
    }

    def __init__(self, *args, **kwargs):
        super(ReportSpider,self).__init__(*args, **kwargs)

        self.fout = open('%s/%s.csv' % (self.LIST_FOLDER,'result'),'wb')
        self.writer = csv.DictWriter(self.fout,self.patterns.keys())
        self.writer.writeheader()
        pass

    def __del__(self):
        super(ReportSpider,self).__del()
        self.fout.close()
        pass

    def _make_formdata(self,page_count):
        return {
            '__EVENTTARGET':'gvAbstract',
            '__EVENTARGUMENT':'Page$' + str(page_count),
        }

    def _make_form_request(self,response,page_count,callback_func):
        return FormRequest.from_response(response,
            formdata = self._make_formdata(page_count),
            meta = {
                'current' : page_count
            },
            callback = callback_func
        )

    def _make_report_list_items(self,response):
        Sel = Selector(response)
        rowSelList = Sel.xpath("//table[@id='gvAbstract']/tr[@class='gridRow']")
        items = []

        def getAttr(selector,pattern):
            result = selector.xpath(pattern).extract()
            return result[0].encode('utf-8') if (len(result)>0) else ''

        patterns = self.patterns

        for rowSel in rowSelList:
            item = {}
            item['HCODE'] = getAttr(rowSel,patterns['HCODE'])
            item['DST'] = getAttr(rowSel,patterns['DST'])
            item['EDN'] = getAttr(rowSel,patterns['EDN'])
            item['DOCTYPE'] = getAttr(rowSel,patterns['DOCTYPE'])
            item['PER'] = getAttr(rowSel,patterns['PER'])
            item['EXTP'] = getAttr(rowSel,patterns['EXTP'])
            item['NOTES'] = getAttr(rowSel,patterns['NOTES'])
            items.append(item)

        return items

    def _write_report_list_items(self,items):
        self.writer.writerows(items)
        pass


    def parse(self,response):
        # Entry the last page
        yield self._make_form_request(response,'Last',self.parse_last_page_num)
        # store page one items
        items = self._make_report_list_items(response)
        self._write_report_list_items(items)

        # entry the next page
        yield self._make_form_request(response,2,self.parse_report_list)

        pass

    def parse_report_list(self,response):
        current = int(response.meta.get('current',1));
        print "Current page:%d Last page: %d\n" %(current,self.last_page_num)

        #open('results/%s' % (str(current)),'wb').write(response.body)

        items = self._make_report_list_items(response)

        self._write_report_list_items(items)

        # go ahead next page
        if (current < self.last_page_num):
            yield self._make_form_request(response,current+1,self.parse_report_list)

        pass

    def parse_last_page_num(self,response):
        selector = Selector(response)
        pages = selector.xpath("//a[contains(@href,'gvAbstract')]/text()").extract()
        self.last_page_num = int(pages[-1])+1
        return
