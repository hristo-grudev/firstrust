import scrapy

from scrapy.loader import ItemLoader

from ..items import FirstrustItem
from itemloaders.processors import TakeFirst


class FirstrustSpider(scrapy.Spider):
	name = 'firstrust'
	start_urls = ['https://www.firstrust.com/blog']

	def parse(self, response):
		post_links = response.xpath('//a[@class="post-cta"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="mid-page-title-italic h-zero"]/text()').get()
		description = response.xpath('//div[@class="blog-body-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="body-text"]/text()').get().split('|')[0] or ''

		item = ItemLoader(item=FirstrustItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
