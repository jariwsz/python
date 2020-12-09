# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CrawlerQuanbenItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    novel_topic = Field()
    novel_name = Field()
    novel_chapter = Field()
    novel_content = Field()
