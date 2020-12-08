# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class YanxuanItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goodsId = Field()        # 商品ID
    goodsTitle = Field()     # 商品标题
    star = Field()          # 评分
    comment = Field()       # 评价内容

    skuInfo = Field()       # SKU
    color = Field()         # 颜色
    size = Field()          # 尺寸

    createTime = Field()    # 创建时间
