import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from zopa.items import Article


class zopaspiderSpider(scrapy.Spider):
    name = 'zopaspider'
    start_urls = ['https://blog.zopa.com/']

    def parse(self, response):
        links = response.xpath('//article//h2/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="post__title"]/text()').get().strip()
        date = " ".join(response.xpath('(//p[@class="post__posted-on"]/text())[1]').get().split()[2:])
        date = datetime.strptime(date, '%d %B %Y')
        date = date.strftime('%Y/%m/%d')
        author = response.xpath('(//p[@class="post__posted-on"]/a)[1]/text()').get()
        category = response.xpath('(//p[@class="post__posted-on"]/a)[2]/text()').get()
        content = response.xpath('//div[@class="post__content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('author', author)
        item.add_value('category', category)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
