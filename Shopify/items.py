# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# items.py

import scrapy

class ProductItem(scrapy.Item):
    # Define the fields for the product item
    title = scrapy.Field()
    price = scrapy.Field()
    discounted_price = scrapy.Field()
    image_urls = scrapy.Field()
    product_url = scrapy.Field()
    ratings = scrapy.Field()
    number_of_reviews = scrapy.Field()


