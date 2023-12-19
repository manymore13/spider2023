# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    quote = scrapy.Field()


# 东方财务研报
class Report(scrapy.Item):
    title = scrapy.Field()
    orgSName = scrapy.Field()
    publishDate = scrapy.Field()
    industryName = scrapy.Field()
    pdfUrl = scrapy.Field()
