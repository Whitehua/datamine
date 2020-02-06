# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DatamineItem(scrapy.Item):
    # define the fields for your item here like:

    pass


class ObjectItem(scrapy.Item):
    gms_title = scrapy.Field();
    gms_url = scrapy.Field();
    gms_spot = scrapy.Field();
    gms_tag = scrapy.Field();
    gms_area = scrapy.Field();
    gms_floor = scrapy.Field();
    gms_buildtime = scrapy.Field();
    gms_totalprice = scrapy.Field();
    gms_unitprice = scrapy.Field();
    gms_market = scrapy.Field();
    gms_district = scrapy.Field();
    gms_shopcircle = scrapy.Field();
    gms_address = scrapy.Field();
    gms_booker = scrapy.Field();
    gms_city = scrapy.Field();

