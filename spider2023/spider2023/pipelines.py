# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import openpyxl


class ExcelPipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

    def close_spider(self, spider):
        self.wb.save('行业研报.xlsx')

    def process_item(self, item, spider):
        self.ws.append((item['title'], item['orgSName'], item['publishDate'], item['industryName'], item['pdfUrl']))
        return item
