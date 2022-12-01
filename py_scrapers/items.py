# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PyScrapersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArizonaPropertyItem(scrapy.Item):
    Name = scrapy.Field()
    Image = scrapy.Field()
    Price = scrapy.Field()
    County = scrapy.Field()
    Agency = scrapy.Field()
    Description = scrapy.Field()
