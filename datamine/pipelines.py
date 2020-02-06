# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

import MySQLdb
import json
import MySQLdb.cursors
from datetime import datetime
import lxml.etree
from numpy.core.defchararray import join


class DataminePipeline(object):
    def __init__(self):
        pass


class MysqldbPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="anjuke", charset="utf8")
        self.cursor = self.conn.cursor()

        SQL1 = """select `city` from spider_city_data """
        self.cursor.execute(SQL1)
        return_city = self.cursor.fetchall()
        a_city = []
        for s in return_city:
            a_city.append('spider_city_data_' + str(s[0]))

        SHOW_TABLE_SQL = """SHOW TABLES"""
        self.cursor.execute(SHOW_TABLE_SQL)
        tables = [self.cursor.fetchall()]

        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        print(table_list)
        for i in range(len(table_list)):
            if a_city[i] in table_list:
                continue
            else:
                SQL = """ Create table """ + str(a_city[i]) + """ (`id` int(11) NOT NULL AUTO_INCREMENT,
                `title` varchar(255) DEFAULT NULL,
                `url` varchar(255) DEFAULT NULL,
                `spot` varchar(100) DEFAULT NULL,
                `tag` varchar(100) DEFAULT NULL,
                `area` varchar(100) DEFAULT NULL,
                `floor` varchar(100) DEFAULT NULL,
                `buildtime` varchar(100) DEFAULT NULL,
                `totalprice` varchar(100) DEFAULT NULL,
                `unitprice` varchar(100) DEFAULT NULL,
                `market` varchar(100) DEFAULT NULL,
                `district` varchar(100) DEFAULT NULL,
                `shopcircle` varchar(100) DEFAULT NULL,
                `address` varchar(255) DEFAULT NULL,
                `booker` varchar(100) DEFAULT NULL,
                `city` varchar(100) DEFAULT NULL,
                `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`)
                ) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='MySQL Foreign Servers table';
                flush privileges;"""
                self.cursor.execute(SQL)
                # 清空表
                self.cursor.execute('truncate table ' + str(a_city[i]) + ';')
        self.conn.commit()

    def process_item(self, item, spider):
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        title = item['gms_title'].replace('\n', '').replace(' ', '').replace('\r', '').replace('\t', '')
        url = item['gms_url']
        spot = item['gms_spot']
        tagone = item['gms_tag']
        area = item['gms_area'].replace('\n', '').replace(' ', '').replace('\r', '').replace('\t', '')
        floor = item['gms_floor'].replace('\n', '').replace(' ', '').replace('\r', '').replace('\t', '')
        buildtime = item['gms_buildtime']
        totalprice = item['gms_totalprice']
        unitprice = item['gms_unitprice'].replace('\n', '').replace(' ', '').replace('\r', '').replace('\t', '')
        cache = item['gms_address']
        booker = item['gms_booker']
        city = item['gms_city']


        SQL1 = """ select `city` from spider_city_data where title = '"""+str(''.join(city))+"""'"""
        self.cursor.execute(SQL1)
        return_city = self.cursor.fetchall()
        a_city = []
        for s in return_city:
            a_city.append(s[0])
        city_name = str(a_city[0])

        spotall = ('-'.join(spot))
        tag = (''.join(tagone))

        ss = (''.join(cache)).split(u'\xa0\xa0 ')
        market = ss[0]
        aa = ss[1].split('-')
        district = aa[0]
        shopcircle = aa[1]
        address = aa[2]
        print(title, url, spotall, tag, area, floor, buildtime, totalprice, unitprice, market, district, shopcircle,
              address, booker,
              city, now)

        SQL = """
                insert IGNORE into spider_city_data_""" + str(city_name) + """ (
                title,url,spot,tag,area,floor,buildtime,totalprice,unitprice,market,district,shopcircle,address,booker,city,datetime)
                value ('"""+title+"""','"""+url+"""','"""+str(spotall)+"""','"""+str(tag)+"""','""" +str(area)+"""',
                '"""+str(floor)+"""','"""+str(buildtime)+"""','"""+str(totalprice)+"""','"""+str(unitprice)+"""',
                '"""+str(market)+"""','"""+str(district)+"""','"""+str(shopcircle)+"""','"""+str(address)+"""',
                '"""+str(booker)+"""','"""+str(city)+"""','"""+str(now)+"""')"""

        self.cursor.execute(SQL)
        self.conn.commit()
        return item;


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('house.json', 'wb')

    def process_item(self, item, spider):
        rep_item = item;
        line = json.dumps(dict(rep_item)).replace('\n', '')
        # self.file.write(line.replace(' ','')+"\n")
        return item;
