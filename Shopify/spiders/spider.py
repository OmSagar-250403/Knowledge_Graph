import scrapy
from scrapy import Request
import json

class ShopifySpider(scrapy.Spider):
    name = "spider"
    start_urls = [
        "https://gymshark.com/products.json",
    ]
    products_limit = 500  # Limit to fetch only 500 products

    custom_settings = {
        'ITEM_PIPELINES': {
            'Shopify.pipelines.CsvWriterPipeline': 300
        }
    }

    def parse(self, response):
        try:
            data = json.loads(response.text)
            products = data.get('products', [])

            for index, product in enumerate(products):
                if index >= self.products_limit:
                    break

                title = product.get('title', 'N/A')
                price = product['variants'][0]['price'] if product.get('variants') else 'N/A'
                image_url = product['images'][0]['src'] if product.get('images') else 'N/A'
                product_url = f"{response.url.split('/products.json')[0]}/products/{product['handle']}"
                product_type = product.get('product_type', 'N/A')
                tags = ", ".join(product['tags']) if 'tags' in product else 'N/A'

                yield {
                    'title': title,
                    'price': price,
                    'image_url': image_url,
                    'product_url': product_url,
                    'product_type': product_type,
                    'tags': tags
                }

                # Stop further processing once the limit is reached
                if index + 1 >= self.products_limit:
                    break

        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse JSON response from {response.url}")
