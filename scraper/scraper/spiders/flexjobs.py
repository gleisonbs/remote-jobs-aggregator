# -*- coding: utf-8 -*-
import scrapy


class FlexjobsSpider(scrapy.Spider):
    name = 'flexjobs'
    allowed_domains = ['flexjobs.com']
    start_urls = ['https://www.flexjobs.com/jobs/web-software-development-programming']

    def parse(self, response):
        for job_title in response.css('h5 > a ::text').getall():
            yield { 'job_title': job_title }

        for next_page in response.css('a.page-link'):
            yield response.follow(next_page, self.parse)
