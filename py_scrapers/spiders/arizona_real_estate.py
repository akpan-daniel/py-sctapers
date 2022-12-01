import scrapy
from scrapy.http import Response
from scrapy.loader import ItemLoader

from py_scrapers.items import ArizonaPropertyItem


class ArizoneSpider(scrapy.Spider):
    name = "arizona"
    allowed_domains = ["arizonarealestate.com"]
    start_urls = ["https://arizonarealestate.com"]

    def parse(self, response: Response):
        counties = response.xpath("//section[@class='section-city-list']//ul[contains(@class, 'list')]/li/a")

        for county in counties:
            next_url = county.xpath("./@href").get()
            county_name = county.xpath("./text()").get()
            yield response.follow(url=next_url, callback=self.parse_property, meta={"name": county_name})

    def parse_property(self, response: Response):
        county = response.meta["name"]
        properties = response.xpath("//div[@class='si-listings-column']")

        for property in properties:
            item = ItemLoader(item=ArizonaPropertyItem(), response=response, selector=property)
            item.add_value("County", county)
            item.add_xpath("Name", ".//div[@class='si-listing__title-main']/text()")
            item.add_xpath("Description", ".//div[@class='si-listing__title-description']/text()")
            item.add_xpath("Agency", ".//div[@class='si-listing__footer']/div/text()")
            item.add_xpath("Price", ".//div[@class='si-listing__photo-price']/span/text()")
            item.add_xpath("Image", ".//img[@class='si-listing-photo']/@src")

            yield item.load_item()

        next_url = response.xpath("//li[@class='next']/@href")
        if next_url:
            yield response.follow(url=next_url, callback=self.parse_property, meta=response.meta)
