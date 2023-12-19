import logging
import os
import csv

from itemadapter import ItemAdapter
from spider2023.items import Report


class CsvPipeline:
    """
    csv Pipeline
    """
    title = ('研报名称', '机构名称', '发布时间', '行业', '研报地址')

    def __init__(self):
        self.item_dic = {}

    def close_spider(self, spider):
        for industry_name, items in self.item_dic.items():
            self.process_report(industry_name, items)

    def process_report(self, industry_name, items):
        """
        process report
        :param industry_name:
        :param items:
        :return:
        """
        logging.debug("industry_name={},item={}".format(industry_name, items))
        dir_name = './gen/{}/'.format(industry_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        report_list_data = []
        title = self.title
        for item in items:
            report_data = {
                title[0]: item['title'],
                title[1]: item['orgSName'],
                title[2]: item['publishDate'],
                title[3]: item['industryName'],
                title[4]: item['pdfUrl'],
            }
            report_list_data.append(report_data)

        with open(os.path.join(dir_name, 'report.csv'), 'w', encoding='utf-8') as file:
            write = csv.DictWriter(file, fieldnames=self.title)
            write.writeheader()
            write.writerows(report_list_data)

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
