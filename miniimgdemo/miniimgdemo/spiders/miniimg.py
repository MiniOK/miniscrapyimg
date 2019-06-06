# -*- coding: utf-8 -*-
import scrapy
from miniimgdemo.items import MiniimgdemoItem
class MiniimgSpider(scrapy.Spider):
    name = 'miniimg'
    allowed_domains = ['699pic.com']
    start_urls = ['http://699pic.com/people.html'] # http://699pic.com/people.html
    print(start_urls)

    def parse(self, response):
        items = MiniimgdemoItem()
        items['image_urls'] = response.xpath('//div[@class="swipeboxEx"]/div[@class="list"]/a/img/@data-original').extract()
        return items


