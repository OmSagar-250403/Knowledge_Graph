# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

class CsvWriterPipeline:
    def __init__(self):
        self.file = open('products.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.file, fieldnames=[
            'index', 'title', 'price', 'image_url', 'product_url', 'product_type', 'tags'
        ])
        self.csv_writer.writeheader()
        self.index = 1

    def process_item(self, item, spider):
        item['index'] = self.index
        self.csv_writer.writerow(item)
        self.index += 1
        return item

    def close_spider(self, spider):
        self.file.close()
