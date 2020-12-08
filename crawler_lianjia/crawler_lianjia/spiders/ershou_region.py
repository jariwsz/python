# -*- coding: utf-8 -*-
from scrapy import Spider,Request
import re
from lxml import etree
import json
from urllib.parse import quote

from crawler_lianjia.items import CrawlerLianjiaItem
from ..utils import REGIONS


class ErshouRegionSpider(Spider):
    name = 'ershou_region'
    allowed_domains = ['sh.lianjia.com']

    def start_requests(self):
        '''根据区域获取所有小区'''
        for region in list(REGIONS.keys()):
            url = "https://sh.lianjia.com/xiaoqu/" + region + "/"
            yield Request(url=url, callback=self.parse, meta={'region':region}) #用来获取页码


    def parse(self, response):
        '''获取区域内小区列表页码总数'''
        region = response.meta['region']
        selector = etree.HTML(response.text)
        sel = selector.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]  # 返回的是字符串字典
        sel = json.loads(sel)  # 转化为字典
        total_pages = sel.get("totalPage")

        '''分别请求每一页'''
        for i in range(int(total_pages)):
            url_page = "https://sh.lianjia.com/xiaoqu/{}/pg{}/".format(region, str(i + 1))
            yield Request(url=url_page, callback=self.parse_xiaoqu, meta={'region':region})

    def parse_xiaoqu(self,response):
        '''分别请求每个小区'''
        selector = etree.HTML(response.text)
        xiaoqu_list = selector.xpath('//ul[@class="listContent"]//li//div[@class="title"]/a/text()')
        for xq_name in xiaoqu_list:
            url = "https://sh.lianjia.com/chengjiao/rs" + quote(xq_name) + "/"
            yield Request(url=url, callback=self.parse_chengjiao, meta={'xq_name':xq_name, 
                                    'region':response.meta['region']})

    def parse_chengjiao(self,response):
        '''每个小区页面内房源列表'''
        xq_name = response.meta['xq_name']
        selector = etree.HTML(response.text)
        content = selector.xpath("//div[@class='page-box house-lst-page-box']")  #有可能为空
        total_pages = 0
        if len(content):
            page_data = json.loads(content[0].xpath('./@page-data')[0])
            total_pages = page_data.get("totalPage")  # 获取总的页面数量
        for i in range(int(total_pages)):
            url_page = "https://sh.lianjia.com/chengjiao/pg{}rs{}/".format(str(i+1), quote(xq_name))
            yield Request(url=url_page, callback=self.parse_content, meta={'region': response.meta['region']})

    def parse_content(self,response):
        selector = etree.HTML(response.text)
        cj_list = selector.xpath("//ul[@class='listContent']/li")


        for cj in cj_list:
            item = CrawlerLianjiaItem()
            item['region'] = REGIONS.get(response.meta['region'])
            href = cj.xpath('./a/@href')  
            if not len(href):
                continue
            item['href'] = href[0]

            content = cj.xpath('.//div[@class="title"]/a/text()') 
            if len(content):
                content = content[0].split()  # 按照空格分割成一个列表
                item['name'] = content[0]
                item['style'] = content[1]
                item['area'] = content[2]

            content = cj.xpath('.//div[@class="houseInfo"]/text()')
            if len(content):
                content = content[0].split('|')
                item['orientation'] = content[0]
                item['decoration'] = content[1]
                if len(content) == 3:
                    item['elevator'] = content[2]
                else:
                    item['elevator'] = '无'

            content = cj.xpath('.//div[@class="positionInfo"]/text()')
            if len(content):
                content = content[0].split()
                item['floor'] = content[0]
                if len(content) == 2:
                    item['build_year'] = content[1]
                else:
                    item['build_year'] = '无'

            content = cj.xpath('.//div[@class="dealDate"]/text()')
            if len(content):
                item['sign_time'] = content[0]

            content = cj.xpath('.//div[@class="totalPrice"]/span/text()')
            if len(content):
                item['total_price'] = content[0]

            content = cj.xpath('.//div[@class="unitPrice"]/span/text()')
            if len(content):
                item['unit_price'] = content[0]

            content = cj.xpath('.//span[@class="dealHouseTxt"]/span/text()')  
            if len(content):
                for i in content:
                    if i.find("房屋满") != -1:  # 找到了返回的是非-1得数，找不到的返回的是-1
                        item['fangchan_class'] = i
                    elif i.find("号线") != -1:
                        item['subway'] = i
                    elif i.find("学") != -1:
                        item['school'] = i
            yield item
