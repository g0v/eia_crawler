from time import time
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest

class ReportSpider(Spider):
    name = "report"
    allowed_domains = ["epa.gov.tw"]
    start_urls = [
        "http://eiareport.epa.gov.tw/EIAWEB/00.aspx"
    ]
    last_page_num = 343

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

    def parse(self,response):
        # Entry the last page
        yield self._make_form_request(response,11,self.parse_report_list)

    def parse_report_list(self,response):
        current = int(response.meta.get('current',0));
        if (current < 50):
            yield self._make_form_request(response,current+10,self.parse_report_list)
        open('results/%s' % (str(current)),'wb').write(response.body)
        return

    def parse_report_summary(self,response):
        print response.body
        pass;

    def parse_last_page(self,response):
        selector = Selector(response)
        pages = selector.xpath("//a[contains(@href,'gvAbstract')]/text()").extract()
        self.last_page_num = int(pages[-1])+1

        # Go to each page and parse it
        for i in range(1,self.last_page_num+1):
            print 'Parse current page: ' + str(i)
            yield self._make_form_request(response,i,self.parse_report_list)

        pass;

