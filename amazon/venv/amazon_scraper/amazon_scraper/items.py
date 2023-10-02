# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_id = scrapy.Field()
    department = scrapy.Field()
    name = scrapy.Field()
    stars = scrapy.Field()
    reviews = scrapy.Field()
    rank = scrapy.Field()
    date = scrapy.Field()
    
    


