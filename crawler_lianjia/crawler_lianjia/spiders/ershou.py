# -*- coding: utf-8 -*-
import scrapy
import json
from ..utils import cookie_parser

# scrapy crawl ershou -a region=sh -a search_key='美女'            0页
# scrapy crawl ershou -a region=sh -a search_key='金地'            X页
# scrapy crawl ershou -a region=sh -a search_key='浦东'            XX页

class ErshouSpider(scrapy.Spider):
    name = 'ershou'
    # allowed_domains = ['lianjia.com']

    def start_requests(self):
        '''爬取初始页'''
        self.region_url = 'https://{region}.lianjia.com/ershoufang/'.format(region = self.region)

        full_url = self.region_url + 'rs' + self.search_key
        yield scrapy.Request(url = full_url, callback = self.parse_1st_list, meta={'search_key': self.search_key})

    def parse_1st_list(self, response):
        '''第一页内容处理'''
        room_list = response.xpath('//li[contains(@class, "LOGCLICKDATA")]/div[contains(@class, "info clear")]')
        # print(room_list)
        for room in room_list:
            # print(room.xpath('./div[@class="title"]/a/text()').get())
            yield scrapy.Request(
                url = room.xpath('./div[@class="title"]/a/@href').get(),
                callback = self.parse_item,
                cookies = cookie_parser()
            )

        page_data = response.xpath('//div[contains(@class, "house-lst-page-box")]/@page-data').get()
        if not page_data is None:
            page_num = json.loads(page_data).get('totalPage')
            for num in range(2, page_num + 1):
                full_url = self.region_url + 'pg' + str(num) + 'rs' + response.meta['search_key']
                print(full_url)
                yield scrapy.Request(url = full_url, callback = self.parse_other_list)

    def parse_other_list(self, response):
        # if response.status == 200:
        # print(response.body)
        room_list = response.xpath('//li[contains(@class, "LOGCLICKDATA")]/div[contains(@class, "info clear")]')
        # print(room_list)
        for room in room_list:
            # print(room.xpath('./div[@class="title"]/a/text()').get())
            yield scrapy.Request(
                url = room.xpath('./div[@class="title"]/a/@href').get(),
                callback = self.parse_item
            )

    def parse_item(self, response):
        yield {
            'title': response.xpath('//h1[@class="main"]/text()').get(),
            'sub': response.xpath('//div[@class="title"]/div[@class="sub"]/text()').get(),
            'total_price': '' + response.xpath('//div[@class="price "]/span[@class="total"]/text()').get() + response.xpath('//div[@class="price "]/span[@class="unit"]/span/text()').get(),
            'unit_price': '' + response.xpath('//div[@class="price "]/div[@class="text"]/div[@class="unitPrice"]/span[@class="unitPriceValue"]/text()').get() + response.xpath('//div[@class="price "]/div[@class="text"]/div[@class="unitPrice"]/span[@class="unitPriceValue"]/i/text()').get(),
            'room_main_info': response.xpath('//div[@class="room"]/div[@class="mainInfo"]/text()').get(),
            'room_sub_info': response.xpath('//div[@class="room"]/div[@class="subInfo"]/text()').get(),
            'area_main_info': response.xpath('//div[@class="area"]/div[@class="mainInfo"]/text()').get(),
            'area_sub_info': response.xpath('//div[@class="area"]/div[@class="subInfo"]/text()').get(),
        }
