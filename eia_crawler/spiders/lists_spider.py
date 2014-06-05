import csv
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest

class ListsSpider(Spider):
    RESULTS_FOLDER = 'results'

    name = "lists"
    allowed_domains = ["epa.gov.tw"]
    start_urls = [
        "http://eiareport.epa.gov.tw/EIAWEB/00.aspx"
    ]
    last_page_num = -1

    patterns = {
            'Id': "td/span[contains(@id,'HCODE')]/text()",
            'Agency': "td/span[contains(@id,'DST')]/text()",
            'Name':"td/span[contains(@id,'EDN')]/@title",
            'DocType': "td/span[contains(@id,'DOCTYPE')]/text()",
            'Taker': "td[6]/text()",
            'Status': "td/span[contains(@id,'EXTP')]/text()",
            'Notes': "td/span[contains(@id,'NOTES')]/@title"
    }

    def __init__(self, *args, **kwargs):
        super(ListsSpider,self).__init__(*args, **kwargs)

        self.fout = open('%s/%s.csv' % (self.RESULTS_FOLDER,self.name),'wb')
        self.writer = csv.DictWriter(self.fout,self.patterns.keys())
        self.writer.writeheader()

        pass

    def __del__(self):
        super(ListsSpider,self).__del()

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

            for attr,pattern in self.patterns.iteritems():
                item[attr] = getAttr(rowSel,pattern)

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
