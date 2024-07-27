from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    # Get Scrapy project settings
    settings = get_project_settings()

    # Optionally, you can override settings here if needed
    settings.update({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'LOG_LEVEL': 'DEBUG'
    })

    # Initialize a CrawlerProcess with your settings
    process = CrawlerProcess(settings)

    # Start the spider by its name ('shopify_spider' in this case)
    process.crawl('spider')

    # Run the process
    process.start()
