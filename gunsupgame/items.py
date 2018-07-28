# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AllianceItem(scrapy.Item):
    url_id = scrapy.Field()
    name = scrapy.Field()


class SeasonItem(scrapy.Item):
    serial_id = scrapy.Field()


class AllianceSeasonPointItem(scrapy.Item):
    alliance_url_id = scrapy.Field()
    season_serial_id = scrapy.Field()
    victory_point = scrapy.Field()
