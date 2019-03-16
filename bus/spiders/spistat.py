from bus.items import SiteItem
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request


def parse_site(response):
    item = SiteItem()
    sel = Selector(response)

    name = sel.xpath('//*[@id="bus_site"]/div[1]/div/div[1]/span[1]/h1/text()').extract()
    item['name'] = name[0]
    # print(name)

    line_num = sel.xpath('//*[@class="bus_i_t3"]/text()').extract()
    item['line_num'] = line_num[0]
    # print(line_num)

    ret = ""
    lines = sel.xpath('//*[@id="bus_site"]/div[1]/div/div[2]/a/text()').extract()
    # print(lines)
    for line in lines:
        ret = ret + " " + line
    item['lines'] = ret

    return item


def parse_page(response):
    print(response.url)
    sel = Selector(response)
    divs = sel.xpath('//*[@id="con_site_1"]/a/@href').extract()
    for dd in divs:
        url = "https://shenzhen.8684.cn" + dd
        yield Request(url, callback=parse_site)


class StationSpider(CrawlSpider):
    name = 'stat_spi'
    start_urls = ['https://shenzhen.8684.cn/sitemap1']

    def parse(self, response):
        sel = Selector(response)
        divs = sel.xpath('//*[@id="site_ul"]/li/a/@href').extract()
        for dd in divs:
            url = "https://shenzhen.8684.cn" + dd
            yield Request(url, callback=parse_page)
