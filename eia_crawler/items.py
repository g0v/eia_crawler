# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class EiaCrawlerItem(Item):
    # define the fields for your item here like:
    title = Field()
    link = Field()
    desc = Field()
    pass
