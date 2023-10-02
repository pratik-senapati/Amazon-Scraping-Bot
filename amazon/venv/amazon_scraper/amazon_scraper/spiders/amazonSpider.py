import scrapy
import datetime
from urllib.parse import urljoin
from amazon_scraper.items import AmazonScraperItem
import regex as re



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
        items = response.css('#gridItemRoot')[:2]
        department=response.xpath('/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[1]/h1/text()').get()
        dep=department.split(' ')[0] if department else None
        count=1
        for item in items:
            name = item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/a/span/div/text()').get().strip()
            stars = item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/div/div/a/@title').get()
            stars_items=float(stars.split(' ')[0]) if stars else 0.0
            reviews = item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/div/div/a/span/text()').get()
            cleaned_reviews = re.sub(r'\D', '', reviews) if reviews else None
            reviews_items=int(cleaned_reviews) if cleaned_reviews else 0
            item_id=item.xpath(f'//*[@id="p13n-asin-index-{count}"]/div[2]/div/@id').get().strip()

            amazon_item = AmazonScraperItem(
                item_id=item_id,
                department=dep,
                name=name,
                stars=stars_items,
                reviews=reviews_items,
                rank=count,
                date=datetime.datetime.now().date()
                )

            yield amazon_item

            count+=1
            
            sub_department_urls = response.css('div[role="treeitem"] a::attr(href)').getall()
            for sub_department_url in sub_department_urls:
                absolute_sub_department_url = urljoin(response.url, sub_department_url)
                yield response.follow(absolute_sub_department_url, callback=self.parse_page)
    
        