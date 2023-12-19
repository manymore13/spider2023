import os.path
import json
from io import TextIOWrapper
from typing import TextIO

from scrapy.exporters import JsonItemExporter
from spider2023.items import Report


class JsonPipeline:

    def __init__(self):
        self.items = []

    def close_spider(self, spider):
        if self.jsonFile is not None:
            self.jsonFile.close()
        self.jsonFile.write(json.dumps(self.items))

    def process_item(self, item, spider):
        if not isinstance(item, Report):
            return item

        path = './gen/{}/'.format(item['industryName'])
        if not os.path.exists(path):
            os.makedirs(path)
        self.jsonFile = open(path + 'report.json', 'w')
        self.items.append(item)

