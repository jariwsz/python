# -*- coding: utf-8 -*-
import scrapy

# scrapy crawl district -o distrcit.csv

class DistrictSpider(scrapy.Spider):
    name = 'district'
    allowed_domains = ['www.stats.gov.cn']
    root_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/'

    def start_requests(self):
        '''爬取初始页'''
        yield scrapy.Request(url = self.root_url, callback = self.parse_root_page)

    '''得到所有省列表'''
    def parse_root_page(self, response):
        province_list = response.xpath('//tr[@class="provincetr"]/td/a')

        for province in province_list:
            # yield {
            #     'name': province.xpath('./text()').get(),
            #     'url': self.root_url + province.xpath('./@href').get(),
            # }
            province_name = province.xpath('./text()').get()
            province_url = self.root_url + province.xpath('./@href').get()
            yield scrapy.Request(url = province_url, callback = self.parse_province_page, meta={'province': province_name})

    '''得到所有市列表'''
    def parse_province_page(self, response):
        province_name = response.meta['province']
        city_list = response.xpath('//tr[@class="citytr"]')

        for city in city_list:
        #     yield {
        #         'city_code': city.xpath('./td[1]/a/text()').get(),
        #         'city_name': city.xpath('./td[2]/a/text()').get(),
        #         'city_url': self.root_url + city.xpath('./td[2]/a/@href').get(),
        #     }
        
            city_name = city.xpath('./td[2]/a/text()').get()
            city_url = self.root_url + city.xpath('./td[2]/a/@href').get()
            yield scrapy.Request(url = city_url, callback = self.parse_city_page, meta={'province': province_name, 'city': city_name})

    '''得到所有区列表'''
    def parse_city_page(self, response):
        province_name = response.meta['province']
        city_name = response.meta['city']

        area_list = response.xpath('//tr[@class="countytr"]/td[1]/a')

        for area in area_list:
            area_code = area.xpath('./text()').get()
            area_name = area.xpath('./../following-sibling::td[1]/a/text()').get()
            area_url = self.root_url + area.xpath('./../following-sibling::td[1]/a/@href').get()
            yield {
                'area_code': area_code,
                'area_name': area_name,
                'area_url': area_url,
            }