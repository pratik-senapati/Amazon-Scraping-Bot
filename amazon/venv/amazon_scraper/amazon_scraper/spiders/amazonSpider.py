import scrapy
import datetime
import hashlib
from amazon_scraper.items import AmazonScraperItem
import regex as re


class AmazonspiderSpider(scrapy.Spider):
  
    name = "amazonSpider"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/gp/bestsellers"]
    visited_urls = set()  # Set to keep track of visited URLs

    def hash_url(self, url):
        # Create an MD5 hash of the URL
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def parse(self, response):
        treeitem_divs = response.css('div[role="treeitem"] a::attr(href)').getall()
        for rel_url in treeitem_divs:
            base_url = 'https://www.amazon.in'
            absolute_url = base_url + rel_url
            url_hash = self.hash_url(absolute_url)
            

            if url_hash not in self.visited_urls:
                self.visited_urls.add(url_hash)  # Add hashed URL to visited set
                yield response.follow(absolute_url, callback=self.parse_page)    
                

                

            
            
            
        
        
    
    
    def parse_page(self, response):
        items = response.css('#gridItemRoot')[:10]
        department=response.xpath('/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[1]/h1/text()').get()
        dep=' '.join(department.split(' ')[2:]) if department else None
       
        
        
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
            
            # Follow links to subcategories and call parse_page for each subcategory page
        sub_category_urls = response.css('div[role="treeitem"] a::attr(href)').getall()
        for sub_category_url in sub_category_urls:
            absolute_sub_category_url = response.urljoin(sub_category_url)
        
            if absolute_sub_category_url not in self.visited_urls:
                self.visited_urls.add(absolute_sub_category_url)  # Add hashed URL to visited set
                #call back the original parse function for further pagination
                yield response.follow(absolute_sub_category_url, callback=self.parse)
            
            
    
        