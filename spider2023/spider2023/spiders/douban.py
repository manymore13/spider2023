# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from spider2023.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response: HtmlResponse, **kwargs):
        # 使用 CSS 选择器提取电影列表
        movies = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        # 遍历每部电影
        for movie in movies:
            item = MovieItem()
            item['title'] = movie.xpath(".//span[@class='title']/text()")[0].get()
            item['rating'] = movie.xpath(".//span[@class='rating_num']/text()").get()
            item['quote'] = movie.xpath(".//p[@class='quote']/span/text()").get()
            yield item
        # 获取其他页面地址
        hrefs = response.xpath("//div[@class='paginator']//a/@href").getall()
        for href in hrefs:
            url = response.urljoin(href)
            yield Request(url)
