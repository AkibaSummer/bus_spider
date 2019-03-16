# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    bus_type = scrapy.Field()
    time = scrapy.Field()
    cost = scrapy.Field()
    company = scrapy.Field()
    update_time = scrapy.Field()
    first_name = scrapy.Field()
    first_line = scrapy.Field()
    second_name = scrapy.Field()
    second_line = scrapy.Field()


class SiteItem(scrapy.Item):
    name = scrapy.Field()
    line_num = scrapy.Field()
    lines = scrapy.Field()
