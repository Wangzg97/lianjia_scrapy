# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymysql import connect

# MongoDB
class MongoPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient()

    def process_item(self, item, spider):
        self.client.lianjia.ershoufang.insert(item)
        spider.number += 1  # 统计下载的记录条数
        return item

    def close_spider(self, spider):
        self.client.close()


# 使用MySQL要提前在相应数据库lianjia建表t_ershoufang
class MySqlPipeline(object):
    def open_spider(self, spider):
        self.client = connect(host="localhost", port=3306, user="root", password="123456", db='lianjia', charset='utf8')
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        args = [
            item['name'],
            item['totalPrice'],
            item['unitPriveValue'],
            item['areaName'],
            item['communityName'],
            item['houseType'],
            item['area'],
            item['decorationSituation'],
            item['floor'],
            item['tradingRight'],
            item['mortgageInformation'],
            item['purpose'],
            item['propertyOwnership'],
            item['propertyRightYears']
        ]
        sql = 'insert into t_ershoufang values(0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.cursor.execute(sql, args)
        self.client.commit()
        spider.number += 1  # 统计下载的记录条数
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()
