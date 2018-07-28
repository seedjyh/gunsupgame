# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from gunsupgame.items import SeasonItem, AllianceItem, AllianceSeasonPointItem


class CurrentSeasonSpider(scrapy.Spider):
    name = 'current_season'
    allowed_domains = ['gunsupgame.com']
    start_urls = ['http://gunsupgame.com/en-us/alliances/leaderboards/current_season']

    # 爬虫入口
    def parse(self, response):
        return Request(response.url, callback=self.parse_season_page)

    # 爬取当前赛季的一页
    def parse_season_page(self, response):
        # 横向：进入下一页
        # （无，暂时只关心首页）
        # 当前：爬取赛季信息
        season_item_loader = ItemLoader(item=SeasonItem(), response=response)
        season_item_loader.add_xpath('serial_id', xpath='//*[@class="current-season-label"]/text()')
        season_item = season_item_loader.load_item()
        yield season_item
        # 当前：爬取当前页信息
        selectors = response.xpath('//*[@class="leaderboard-table"]/tbody/tr')
        for selector in selectors:
            for item in self.parse_season_page_line(selector=selector, season_serial_id=season_item['serial_id']):  # 扁平化
                yield item

    # 解析当前赛季页的一行
    @staticmethod
    def parse_season_page_line(selector, season_serial_id):
        data_selectors = selector.xpath('./td')
        # [0] => 当前排名
        # [1] => 联盟名字等信息
        alliance_item_loader = ItemLoader(item=AllianceItem(), selector=data_selectors[1])
        alliance_item_loader.add_xpath('name', xpath='./a/text()')
        alliance_item_loader.add_xpath('url_id', xpath='./a/@href', re='.*\/([0-9]+)$')
        alliance_item = alliance_item_loader.load_item()
        yield alliance_item
        # [4] => 当前胜利点数
        alliance_season_point_item_loader = ItemLoader(item=AllianceSeasonPointItem(), selector=data_selectors[4])
        alliance_season_point_item_loader.add_value('alliance_url_id', alliance_item['url_id'])
        alliance_season_point_item_loader.add_value('season_serial_id', season_serial_id)
        alliance_season_point_item_loader.add_xpath('victory_point', xpath='./text()[2]')
        alliance_season_point_item = alliance_season_point_item_loader.load_item()
        yield alliance_season_point_item
