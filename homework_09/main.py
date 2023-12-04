import json

import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()


class QuotesPipeline:
    authors = []
    quotes = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "fullname" in adapter.keys():
            self.authors.append(
                {
                    "fullname": adapter["fullname"],
                    "born_date": adapter["born_date"],
                    "born_location": adapter["born_location"],
                    "description": adapter["description"],
                }
            )
        elif "quote" in adapter.keys():
            self.quotes.append(
                {
                    "tags": adapter["tags"],
                    "author": adapter["author"],
                    "quote": adapter["quote"],
                }
            )
        return item

    def close_spider(self, spider):
        with open("src\\authors.json", "w", encoding="utf-8") as fd:
            json.dump(self.authors, fd, ensure_ascii=False)
        with open("src\\quotes.json", "w", encoding="utf-8") as fd:
            json.dump(self.quotes, fd, ensure_ascii=False)


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    custom_settings = {"ITEM_PIPELINES": {QuotesPipeline: 300}}

    def parse(self, response, *_):
        for item in response.xpath("/html//div[@class='quote']"):
            tags = item.xpath("div[@class='tags']/a/text()").extract()
            author = item.xpath("span/small/text()").get().strip()
            quote = item.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(tags=tags, author=author, quote=quote)
            yield response.follow(
                url=self.start_urls[0] + item.xpath("span/a/@href").get(),
                callback=self.nested_parse,
            )
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse(self, response, *_):
        author = response.xpath("/html//div[@class='author-details']")
        fn = author.xpath("h3[@class='author-title']/text()").get().strip()
        bd = author.xpath("p/span[@class='author-born-date']/text()").get().strip()
        bl = author.xpath("p/span[@class='author-born-location']/text()").get().strip()
        desc = author.xpath("div[@class='author-description']/text()").get().strip()
        yield AuthorItem(fullname=fn, born_date=bd, born_location=bl, description=desc)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
