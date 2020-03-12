# -*- coding: utf-8 -*-
import scrapy


class DarmerSpider(scrapy.Spider):
    name = 'darmer'
    allowed_domains = ['www.yuewz.com']
    start_urls = ['http://www.yuewz.com/']

    def parse(self, response):
        pass
