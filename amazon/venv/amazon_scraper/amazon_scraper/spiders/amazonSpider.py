import scrapy
import datetime
from urllib.parse import urljoin




class AmazonspiderSpider(scrapy.Spider):
    name = "amazonSpider"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/gp/bestsellers"]
    
    
    def parse(self, response):
        treeitem_divs = response.css('div[role="treeitem"] a::attr(href)').getall()
        for rel_url in treeitem_divs:
            base_url = 'https://www.amazon.in'
            absolute_url =base_url+rel_url
            yield response.follow(absolute_url, callback=self.parse_page)
            
            
        
        
    
    
    def parse_page(self, response):
        items = response.css('#gridItemRoot')[:10]
        department=response.xpath('/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[1]/h1/text()').get().split(' in ')[1]
        count=1
        for item in items:
            name = item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/a/span/div/text()').get().strip()
            stars = item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/div/div/a/@title').get()
            stars_item=stars.split(' ')[0]  if stars else 0
            stars_item=stars if stars else 0
            reviews = item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/div/div/a/span/text()').get()
            reviews_item=reviews if reviews else 0
            item_id=item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/@id').get().strip()

            
            yield {
                'item_id':item_id,
                'department':department,
                'name': name,
                'stars': stars_item, 
                'reviews': reviews_item,
                'rank':count,
                'date': datetime.datetime.now().date(),
            }

            count+=1
    
        