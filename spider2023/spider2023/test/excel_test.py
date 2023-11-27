import openpyxl


class ExcelPipeline:
    title = ('研报名称', '机构名称', '发布时间', '行业', '研报地址')

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

    def close_spider(self):
        self.wb.save('行业研报.xlsx')

    def process_item(self, item, spider):

        self.ws.append((item['title'], item['orgSName'], item['publishDate'], item['industryName'], item['pdfUrl']))

        return item


if __name__ == '__main__':
    wb = openpyxl.Workbook()
    ws = wb.active
    ws1 = wb['model']
    print(ws1)
    wb.get_sheet_by_name('test')
    wb.save('test.xlsx')
    print(ws)
