# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AmazonScraperPipeline:
    def process_item(self, item, spider):
        
        adapter=ItemAdapter(item)
        
        from itemadapter import ItemAdapter
import datetime

class AmazonScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Clean and process the 'stars' field
        stars = adapter.get('stars')
        adapter['stars'] = float(stars.split(' ')[0]) if stars else None
        
        # Clean and process the 'reviews' field
        reviews = adapter.get('reviews')
        adapter['reviews'] = int(reviews.strip()) if reviews else None
        
        
        

       

        return item

        
        
