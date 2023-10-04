# Amazon-Scraping-Bot
An Amazon Web Scraping Bot that uses Scrapy to Scrape the data from the bestseller page on a daily basis

This Amazon Scraping Bot was built with the Python Framework Scrapy

It uses ScrapeOps API to generate fake user agents so that amazon doesn't block all our requests

The data is stored in a file called items.json and each line of data consists of:
    ->Item ID
    ->Department
    ->Name
    ->Stars
    ->Reviews
    ->Rank
    ->Date

There is also another file called links.json that has links to all the departments separately

Commands you need to successfully run the Scraper on your own PC are:

->Install Scrapy
pip install Scrapy

->Create a Virtual Environment 
python -m venv venv

->Activate the Virtual Environment
venv\Scripts\activate

when above the venv directory

->This is to create a new project, but that is not required
scrapy startproject amazon_scraper


->To allow the scraper to work, make an account on ScrapeOps to get your very own API key and enter it here:

    SCRAPEOPS_API_KEY='YOUR_API_KEY'

    in the settings.py file

->To run:

    scrapy crawl amazonSpider -O items.json

    this overwrites the items.json file
    you may also run it as -o to append on to the file when executing for different days 

This took me a couple of days to build, and I learnt a lot
I hope to build a full website that lets you scrape amazon or a similar website
with a fun UI/UX in the MERN stack since that is what I'm learning right now.




