# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from es_type import Comment
# 去除html　tags
from w3lib.html import remove_tags

class ElasticsearchPipeline:
    def process_item(self, item, spider):
        # 将item转换为ES的数据
        comment = Comment()

        comment.goodsId = item['goodsId']
        comment.goodsTitle = item['goodsTitle']
        comment.star = item['star']
        comment.content = item['comment']
        comment.skuInfo = item['skuInfo']
        comment.size = item['size']
        comment.color = item['color']
        comment.createTime = item['createTime']

        comment.save()

        return item
