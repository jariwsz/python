# -*- coding:utf-8 -*-

from elasticsearch_dsl import connections, Document, Completion, Text, Long, Date, Keyword, analyzer, token_filter


# 执行python .\es_type.py初始化



# 新建连接
connections.create_connection(hosts="127.0.0.1")

class Comment(Document):
    # 商品ID
    goodsId = Keyword()
    # 商品标题
    goodsTitle = Text(analyzer="ik_max_word", fields={'raw': Keyword()})
    # 评分
    star = Long()
    # 评论内容
    content = Text(analyzer="ik_max_word", fields={'raw': Keyword()})
    # SKU
    skuInfo = Text(analyzer="ik_max_word", fields={'raw': Keyword()})
    # 颜色
    color = Keyword()
    # 尺寸
    size = Keyword()
    # 创建时间
    createTime = Date()

    class Index:
        # index名称
        name = "yanxuan"

if __name__ == '__main__':
    Comment.init()