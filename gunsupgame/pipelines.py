# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from gunsupgame.items import AllianceItem, SeasonItem, AllianceSeasonPointItem


class GunsupgamePipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLPipeline(object):
    def open_spider(self, spider):
        self.db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='gunsupgame',
            charset='utf8'
        )
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.commit()
        self.db.close()

    def process_item(self, item, spider):
        switcher = {
            AllianceItem: self.process_alliance_item,
            SeasonItem: self.process_season_item,
            AllianceSeasonPointItem: self.process_alliance_season_point_item,
        }
        switcher.get(type(item), lambda: "")(item, spider)
        return item

    def process_alliance_item(self, item, spider):
        values = (
            item.get('url_id'),
            item.get('name')
        )
        self.cursor.execute("INSERT IGNORE INTO alliance(url_id, name) VALUES(%s,%s)", values)

    def process_season_item(self, item, spider):
        values = (
            [str.strip(x) for x in item.get('serial_id')],
        )
        self.cursor.execute("INSERT IGNORE INTO season(serial_id) VALUES(%s)", values)

    def process_alliance_season_point_item(self, item, spider):
        values = (
            item.get('alliance_url_id'),
            [str.strip(x) for x in item.get('season_serial_id')],
            [str.strip(x) for x in item.get('victory_point')],
        )
        self.cursor.execute(
            "INSERT IGNORE INTO alliance_season_point(alliance_id, season_id, crawl_time, victory_point) VALUES((select id from alliance where url_id=%s), (select id from season where serial_id=%s), NOW(), %s)",
            values)
