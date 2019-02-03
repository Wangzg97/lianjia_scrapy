# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals

class ErshoufangSpider(scrapy.Spider):
    name = 'ershoufang'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://nj.lianjia.com/ershoufang/pg{}/'.format(page) for page in range(1, 2)]  # 100页

    # using signals
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ErshoufangSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider.number = 0  # 统计下载的记录条数，初始为0
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        spider.logger.info('========>已下载记录条数: %s', spider.number)

    def parse(self, response):
        urls = response.xpath('//div[@class="info clear"]/div/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_info)

    def parse_info(self, response):
        # 具体含义见下面注释
        name = response.xpath('//h1/text()').extract_first()
        totalPrice = response.xpath(
            'concat(//span[@class="total"]/text(),//span[@class="unit"]/span/text())').extract_first()
        unitPriveValue = response.xpath('string(//span[@class="unitPriceValue"])').extract_first()
        communityName = response.xpath('string(//div[@class="communityName"]/a[1])').extract_first()
        areaName = response.xpath('string(//div[@class="areaName"]/span[2])').extract_first().replace('\xa0', '-')
        houseType = response.xpath('string(//div[@class="base"]/div[@class="content"]/ul/li[1]/text())').extract_first()
        area = response.xpath('string(//div[@class="base"]/div[@class="content"]/ul/li[3]/text())').extract_first()
        floor = response.xpath('string(//div[@class="base"]/div[@class="content"]/ul/li[2]/text())').extract_first()
        tradingRight = response.xpath(
            'string(//div[@class="transaction"]/div[@class="content"]/ul/li[2]/span[2]/text())').extract_first()
        mortgageInformation = response.xpath(
            'string(//div[@class="transaction"]/div[@class="content"]/ul/li[7]/span[2]/text())').extract_first() \
            .replace('\n                              ', '')
        purpose = response.xpath(
            'string(//div[@class="transaction"]/div[@class="content"]/ul/li[4]/span[2]/text())').extract_first()
        decorationSituation = response.xpath(
            'string(//div[@class="base"]/div[@class="content"]/ul/li[9]/text())').extract_first()
        propertOwnership = response.xpath(
            'string(//div[@class="transaction"]/div[@class="content"]/ul/li[6]/span[2]/text())').extract_first()
        propertyRightYears = response.xpath(
            'string(//div[@class="base"]/div[@class="content"]/ul/li[12]/text())').extract_first()

        yield {
            "name": name,  # 名称
            "totalPrice": totalPrice,  # 总价格
            "unitPriveValue": unitPriveValue,  # 每平米价格
            "areaName": areaName,  # 所在区名
            "communityName": communityName,  # 小区
            "houseType": houseType,  # 户型
            "area": area,  # 面积
            "decorationSituation": decorationSituation,  # 装修情况
            "floor": floor,  # 楼层
            "tradingRight": tradingRight,  # 交易权属
            "mortgageInformation": mortgageInformation,  # 抵押信息
            "purpose": purpose,  # 房屋用途
            "propertyOwnership": propertOwnership,  # 产权所属
            "propertyRightYears": propertyRightYears  # 产权年限
        }
