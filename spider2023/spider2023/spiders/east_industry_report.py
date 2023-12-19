# -*- coding: utf-8 -*-
import json
import logging
import re
import time

import scrapy
from scrapy import Request
from scrapy import cmdline
from scrapy.http import Response
from spider2023.items import Report


class EastIndustryReportSpider(scrapy.Spider):
    """
    东财行业财报爬取
    """

    name = "east_industry_report"

    east_money_url: str = 'https://reportapi.eastmoney.com/report/list?cb=datatable1808538&industryCode={' \
                          'industry_code}&pageSize={page_size}&industry=*&rating=*&ratingChange=*&beginTime={' \
                          'begin_time}&endTime={end_time}&pageNo={page_no}&fields=&qType=1&orgCode=&rcode=&_={time}'

    report_info_url = 'https://data.eastmoney.com/report/zw_industry.jshtml?infocode='

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.industry_code_list = getattr(self, "codes", '*,738').split(',')
        self.page_size: int = getattr(self, "page_size", '50')
        self.begin_time = getattr(self, "begin_time", '2023-11-26')
        self.end_time: str = getattr(self, "end_time", '2023-11-26')
        self.page_no: str = getattr(self, "page_no", 1)
        self.industry_code_dic = self.load_industry()
        logging.debug("begin get {},page_size={},begin_time={},end_time={},page_no={}".format(self.industry_code_list,
                                                                                              self.page_size,
                                                                                              self.begin_time,
                                                                                              self.end_time,
                                                                                              self.page_no))
        logging.debug("industry_code_dic: {}".format(self.industry_code_dic))

    def start_requests(self):
        logging.debug('start_requests')
        cur_time = int(time.time())
        for industry_code in self.industry_code_list:
            final_report_url = self.east_money_url.format(industry_code=industry_code, page_size=self.page_size,
                                                          begin_time=self.begin_time, end_time=self.end_time,
                                                          page_no=self.page_no, time=cur_time)
            yield Request(url=final_report_url, meta={'req_industry_code': industry_code})
            logging.debug('final_url =' + final_report_url)

    def parse(self, response, **kwargs):
        report_content = re.search('\((.+)\)', response.text).group(1)
        report_json = json.loads(report_content)
        report_list = report_json['data']
        total_page = report_json['TotalPage']
        size = report_json['size']
        logging.debug('total={},size={}'.format(total_page, size))
        for report in report_list:
            title = report['title']
            orgSName = report['orgSName']
            publishDate = re.findall('\d+-\d+-\d+', report['publishDate'])[0]
            industryName = report['industryName']
            pdfUrl = self.report_info_url + report['infoCode']
            report = Report(title=title, orgSName=orgSName, publishDate=publishDate,
                            industryName=industryName, pdfUrl=pdfUrl)
            # report['tableName'] = self.industry_code_dic[response.meta['req_industry_code']]
            logging.debug('pdf_url= ' + pdfUrl)
            yield Request(url=pdfUrl, callback=self.parse_pdf, cb_kwargs={'report': report}, dont_filter=True)

    def parse_pdf(self, response: Response, report: Report):
        """
        解析pdf
        :param response:
        :param report:
        :return:
        """
        pdf_url = response.xpath('//span[@class="to-link"]/a[@class="pdf-link"]/@href')[0].get()
        report['pdfUrl'] = pdf_url
        yield report

    @classmethod
    def load_industry(cls):
        file_name = './industry.json'
        with open(file_name, 'r', encoding='utf-8') as f:
            industry_name_list = json.load(f)
        industry_code_dic = {}
        for industry in industry_name_list:
            industry_code_dic[industry['industry_code']] = industry['industry_name']
        return industry_code_dic


if __name__ == '__main__':
    args = ('scrapy crawl -O east.json -a codes=1045,1046 -a page_size=2 -a begin_time=2023-12-18 -a '
            'end_time=2023-12-19 -a page_no=1 east_industry_report').split()
    cmdline.execute(args)
