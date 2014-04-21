from time import time
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest

class ReportSpider(BaseSpider):
    name = "report"
    allowed_domains = ["epa.gov.tw"]
    start_urls = [
    "http://eiareport.epa.gov.tw/EIAWEB/00.aspx"
    ]
    last_page_num = -1

    def _make_formdata(self,page_count):
        return {
            '__EVENTTARGET':'gvAbstract',
            '__EVENTARGUMENT':'Page$' + str(page_count)

        }

    def _make_form_request(self,response,page_count,callback_func):
        return FormRequest.from_response(response,
            formdata = self._make_formdata(page_count),
            callback = callback_func
        )

    def parse(self,response):
        # Entry the last page
        #yield self._make_form_request(response,'Last',self.parse_last_page)

        self.last_page_num = 343

        for i in range(1,self.last_page_num+1):
            print 'Parse current page: ' + str(i)
            yield self._make_form_request(response,i,self.parse_report_list)

    def parse_report_list(self,response):
        #selector = HtmlXPathSelector(reponse)
       	open(str(time()),'wb').write(response.body)
        pass;

    def parse_report_summary(self,response):
        pass;

    def parse_last_page(self,response):
        selector = HtmlXPathSelector(response)
        pages = selector.select("//a[contains(@href,'gvAbstract')]/text()").extract()
        self.last_page_num = int(pages[-1])+1

        # Go to each page and parse it
        for i in range(1,self.last_page_num+1):
            print 'Parse current page: ' + str(i)
            yield self._make_form_request(response,i,self.parse_report_list)

        pass;

