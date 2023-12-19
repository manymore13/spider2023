from datetime import datetime

from scrapy import cmdline
endTime = datetime.now().strftime('%Y-%m-%d')
args = ('scrapy crawl -a codes=727,1046,438,737,456 -a page_size=50 -a begin_time=2022-12-01 -a '
        'end_time=2023-12-19 -a page_no=1 east_industry_report').split()
cmdline.execute(args)
