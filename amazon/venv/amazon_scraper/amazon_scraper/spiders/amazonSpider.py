import scrapy
import datetime


class AmazonspiderSpider(scrapy.Spider):
    name = "amazonSpider"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/gp/bestsellers/grocery/4859478031/ref=zg_bs_nav_grocery_1"]

    
    def parse(self, response):
        
        items = response.css('#gridItemRoot')[:10]
        count=1
        for item in items:
            name = item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/a/span/div/text()').get().strip()
            stars = item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/div/div/a/@title').get()
            reviews = item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/div/div/a/span/text()').get()

            yield {
                'name': name,
                'stars': stars.strip() if stars else None,
                'reviews': reviews.strip() if reviews else None,
                'rank':count,
                'date': datetime.datetime.now().date()
            }

            count+=1