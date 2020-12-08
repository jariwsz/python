import json
from scrapy import Spider,Request
import re
from yanxuan.items import YanxuanItem



# 搜索页http://you.163.com/xhr/search/search.json?keyword=儿童医用口罩&page=1
# 评论页https://you.163.com/xhr/comment/listByItemByTag.json?itemId=3993436&page=1&size=20
# scrapy crawl 163yanxuan -a keyword='男士内裤' -a size=10
# 注意yield仅能response方法内部使用

class A163yanxuanSpider(Spider):
    name = '163yanxuan'


    def start_requests(self):
        '''爬取初始页'''
        goods_1st_url = 'http://you.163.com/xhr/search/search.json?keyword={keyword}&size={size}&page=1'.format(keyword = self.keyword, size= self.size)
        
        yield Request(url = goods_1st_url, callback = self.parse_goods_1st_page, meta={'keyword': self.keyword, 'size': self.size})

    def parse_goods_1st_page(self, response):
        '''处理商品列表页(第一页)数据'''
        # 首先处理本页数据
        searcherResult = json.loads(response.text)['data']['directly']['searcherResult']
        result = searcherResult['result']

        '''处理每个商品数据'''
        for goods in result:
            # 准备爬取第一页评论数据
            goodsId = goods['id']
            goodsTitle = goods['name']
            size = 10
            comment_1st_url = 'https://you.163.com/xhr/comment/listByItemByTag.json?itemId={goodsId}&page=1&size={size}'.format(goodsId = goodsId, size = size)
            yield Request(url = comment_1st_url, callback = self.parse_comment_1st_page, meta={'goodsId': goodsId, 'goodsTitle': goodsTitle, 'size': size})


        # 其次看还有多少页，继续发出请求
        totalPage = (int)(searcherResult['pagination']['totalPage'])

        # 超过1页需要处理其他页
        if (totalPage > 1):
            for i in range(2, totalPage+1):
                goods_url = 'http://you.163.com/xhr/search/search.json?keyword={keyword}&size={size}&page={page}'.format(keyword = response.meta['keyword'], page = i, size = response.meta['size'])
                yield Request(url = goods_url, callback = self.parse_goods)


    def parse_goods(self, response):
        '''处理商品列表页数据'''
        searcherResult = json.loads(response.text)['data']['directly']['searcherResult']
        result = searcherResult['result']

        '''处理每个商品数据'''
        for goods in result:
            # 准备爬取第一页评论数据
            goodsId = goods['id']
            goodsTitle = goods['name']
            size = 10
            comment_1st_url = 'https://you.163.com/xhr/comment/listByItemByTag.json?itemId={goodsId}&page=1&size={size}'.format(goodsId = goodsId, size = size)
            yield Request(url = comment_1st_url, callback = self.parse_comment_1st_page, meta={'goodsId': goodsId, 'goodsTitle': goodsTitle, 'size': size})


    def parse_comment_1st_page(self, response):
        '''处理评论列表页(第一页)数据'''
        goodsId = response.meta['goodsId']
        goodsTitle = response.meta['goodsTitle']

        # 首先处理本页数据
        data = json.loads(response.text)['data']

        commentList = data['commentList']

        for comment in commentList:
            item = self.handle_comment_list(comment, goodsId, goodsTitle)

            if (item['color'] != '') and (item['size'] != ''):
                yield item


        # 其次看还有多少页，继续发出请求
        totalPage = (int)(data['pagination']['totalPage'])

        # 超过1页需要处理其他页
        if (totalPage > 1):
            for i in range(2, totalPage + 1):
                comment_url = 'https://you.163.com/xhr/comment/listByItemByTag.json?itemId={goodsId}&page={page}&size={size}'.format(goodsId = goodsId, page = i, size = response.meta['size'])
                yield Request(url = comment_url, callback = self.parse_comment, meta={'goodsId': goodsId, 'goodsTitle': goodsTitle})


    def parse_comment(self, response):
        '''处理评论列表页数据'''
        goodsId = response.meta['goodsId']
        goodsTitle = response.meta['goodsTitle']

        data = json.loads(response.text)['data']

        commentList = data['commentList']

        for comment in commentList:
            item = self.handle_comment_list(comment, goodsId, goodsTitle)

            if (item['color'] != '') and (item['size'] != ''):
                yield item


    def handle_comment_list(self, comment, goodsId, goodsTitle):
        item = YanxuanItem()
        
        item['goodsId'] = goodsId
        item['goodsTitle'] = goodsTitle

        item['star'] = comment['star']
        item['comment'] = comment['content']

        item['skuInfo'] = comment['skuInfo']

        item['size'] = ''
        item['color'] = ''
        for sku in item['skuInfo']:
            if sku.startswith('颜色'):
                item['color'] = sku.lstrip('颜色:')
            elif sku.startswith('尺码'):
                item['size'] = sku.lstrip('尺码:')

        item['createTime'] = comment['createTime']

        return item