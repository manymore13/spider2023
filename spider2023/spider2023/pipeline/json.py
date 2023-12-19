import logging
import os.path
import json

from itemadapter import ItemAdapter
from spider2023.items import Report


class JsonPipeline:
    """
    json pipeline
    """

    def __init__(self):
        self.item_dic = {}

    def close_spider(self, spider):
        for industry_name, items in self.item_dic.items():
            logging.debug("industry_name={},item={}".format(industry_name, items))
            dir_name = './gen/{}/'.format(industry_name)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            with open(os.path.join(dir_name, 'report.json'), 'w', encoding='utf-8') as file:
                file.write(json.dumps(items))

    def process_item(self, item, spider):
        if not isinstance(item, Report):
            return item
        industry_name = item['industryName']
        items = self.item_dic.get(industry_name)
        if items is None:
            items = []
        items.append(ItemAdapter(item).asdict())
        self.item_dic[industry_name] = items
        return item
