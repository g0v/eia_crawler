# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ReportSummaryItem(Item):
    # define the fields for your item here like:
    HCODE = Field()
    DST = Field()
    EDN = Field()
    DOCTYPE = Field()
    PER = Field()
    EXTP = Field()
    NOTES = Field()
    pass
