import scrapy
from datamine.items import ObjectItem
from scrapy.spiders import CrawlSpider
import MySQLdb.cursors


class Spider(CrawlSpider):
    '''
        自定义配置 加载个人管道
        '''
    custom_settings = {
        'ITEM_PIPELINES': {
            'datamine.pipelines.JsonWriterPipeline': 333,
            'datamine.pipelines.MysqldbPipeline': 500
        }
    }
    name = "anjuke"
    allowed_domains = ["anjuke.com"]

    # 城市分站
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="anjuke", charset="utf8")
    cursor = conn.cursor()
    SQL1 = """ select `city` from spider_city_data """
    cursor.execute(SQL1)
    all_city = cursor.fetchall()
    list_city = []
    for s in all_city:
        list_city.append(s[0])
    SQL2 = """ select `url` from spider_city_data """
    cursor.execute(SQL2)
    all_url = cursor.fetchall()
    list_city_url = []
    for s in list_city_url:
        list_city_url.append(s[0])
    #print(list_city,list_city_url)
    conn.commit()



    arr_list = []
    for item in list_city:
        arr_list += ['https://' + item + '.anjuke.com/sale/?from=navigation']
        # 计算分页数量
        i, j = 1, 50
        while i < j:
            arr_list += ['https://' + item + '.anjuke.com/sale/p' + str(i)+'/#filtersort']
            i += 1
    start_urls = arr_list

    # 数据抓取部分
    def parse(self, response):
        q=0
        for sel in response.xpath('//li[@class="list-item"]'):
            item = ObjectItem()

            # 标题
            gms_scrapy_1 = sel.xpath('normalize-space(div[@class="house-details"]/div[@class="house-title"]/a/text())').extract_first()
            # 超链接
            gms_scrapy_2 = sel.xpath('div[@class="house-details"]/div[@class="house-title"]/a[1]/@href').extract_first()

            # 户型
            gms_scrapy_3 = sel.xpath('normalize-space(div[@class="house-details"]/div[@class="details-item"]/span[1]/text())').extract()
            # 平米
            gms_scrapy_4 = sel.xpath('div[@class="house-details"]/div[@class="details-item"]/span[2]/text()').extract_first()
            # 层数
            gms_scrapy_5 = sel.xpath('div[@class="house-details"]/div[@class="details-item"]/span[3]/text()').extract_first()
            # 年限
            gms_scrapy_6 = sel.xpath('div[@class="house-details"]/div[@class="details-item"]/span[4]/text()').extract_first()


            # 楼盘
            gms_scrapy_9 = sel.xpath(
                    'normalize-space(div[@class="house-details"]/div[@class="details-item"]/span[@class="comm-address"]/text())').extract_first()
            # 区域
            gms_scrapy_10 = sel.xpath(
                    'normalize-space(div[@class="house-details"]/div[@class="details-item"]/span[@class="comm-address"]/text())').extract_first()
            # 所属商圈
            gms_scrapy_11 = sel.xpath(
                    'normalize-space(div[@class="house-details"]/div[@class="details-item"]/span[@class="comm-address"]/text())').extract_first()
            # 地址
            gms_scrapy_12 = sel.xpath(
                    'normalize-space(div[@class="house-details"]/div[@class="details-item"]/span[@class="comm-address"]/text())').extract()
            #print(gms_scrapy_9+'\n',gms_scrapy_10+'\n')

            # 价格
            gms_scrapy_7 = sel.xpath('div[@class="pro-price"]/span/strong/text()').extract_first()
            # 单价
            gms_scrapy_8 = sel.xpath('div[@class="pro-price"]/span[@class="unit-price"]/text()').extract_first()

            # 联系人
            gms_scrapy_13 = sel.xpath('div[@class="house-details"]/div[@class="broker-item"]/span[@class="broker-name broker-text"]/text()').extract_first()

            gms_scrapy_14 = sel.xpath('div[@class="house-details"]/div[@class="tags-bottom"]/span/text()').extract()

            gms_scrapy_15 = response.xpath('//span[@class="city"]/text()').extract_first()

            item['gms_title'] = gms_scrapy_1
            item['gms_url'] = gms_scrapy_2
            item['gms_spot'] = gms_scrapy_14
            item['gms_tag'] = gms_scrapy_3
            item['gms_area'] = gms_scrapy_4
            item['gms_floor'] = gms_scrapy_5
            item['gms_buildtime'] = gms_scrapy_6
            item['gms_totalprice'] = gms_scrapy_7
            item['gms_unitprice'] = gms_scrapy_8
            item['gms_market'] = gms_scrapy_9
            item['gms_district'] = gms_scrapy_10
            item['gms_shopcircle'] = gms_scrapy_11
            item['gms_address'] = gms_scrapy_12
            item['gms_booker'] = gms_scrapy_13
            item['gms_city'] = gms_scrapy_15
            #print(item)
            yield item
            q=q+1
