import scrapy
from crawler_quanben.items import CrawlerQuanbenItem


class QbSpider(scrapy.Spider):
    name = 'qb_hot'
    allowed_domains = ['www.xqb5200.com']
    start_urls = ['https://www.xqb5200.com/']

    # 一级解析：获取分类下热点小说名称及链接
    def parse(self, response):
        # [position()>1 and position()<14]
        topic_list = response.xpath('//div[@class="novelslist"]/div[contains(@class, "content")]')
        for topic in topic_list:
            novel_topic = topic.xpath('./h2/text()').get()
            novel_list = topic.xpath('./ul/li')
            for novel in novel_list:
                novel_name = novel.xpath('./a/@title').get()
                link = novel.xpath('./a/@href').get()

                yield scrapy.Request(
                url=link,
                meta={'novel_topic':novel_topic, 'novel_name':novel_name, 'novel_url': link},
                callback=self.parse_chapter
            )
 
    # 二级解析：获取小说章节
    def parse_chapter(self, response):
        novel_topic = response.meta['novel_topic']
        novel_name = response.meta['novel_name']
        novel_url = response.meta['novel_url']

        chapter_list=response.xpath('//div[@id="list"]/dl/dd')
        for chapter in chapter_list:
            novel_chapter=chapter.xpath('./a/text()').get()
            # 不同网站的章节处理方式不一样，有些是绝对路径，有些是相对路径
            # 如果是相对路径就需要拼接
            chapter_url = chapter.xpath('./a/@href').get()

            if chapter_url is not None:
                link= novel_url + chapter_url
                yield scrapy.Request(
                url=link,
                meta={'novel_topic':novel_topic,'novel_name':novel_name,'novel_chapter':novel_chapter},
                callback=self.parse_content
            )
            
 
    # 三级解析：获取小说内容
    def parse_content(self,response):
        novel_topic = response.meta['novel_topic']
        novel_name = response.meta['novel_name']
        novel_chapter = response.meta['novel_chapter']
 
        item = CrawlerQuanbenItem()
        item['novel_topic']= novel_topic
        item['novel_chapter'] = novel_chapter
        item['novel_name'] = novel_name
        item['novel_content']=response.xpath('//div[@id="content"]/text()').extract()
 
        yield item
