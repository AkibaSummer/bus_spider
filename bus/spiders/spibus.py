from bus.items import BusItem
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request


def parse_aline(item):
    items = item.xpath('div')
    a = ""
    for dd in items:
        ids = dd.xpath('i/text()').extract()
        stations = dd.xpath('a/text()').extract()
        a = a + ids[0] + ":" + stations[0] + "\n"
    # type: str
    return a


def print_item(item):
    print(item['name'])
    print(item['bus_type'])
    print(item['cost'])
    print(item['company'])
    print(item['update_time'])
    print(item['first_name'])
    print(item['first_line'])
    print(item['second_name'])
    print(item['second_line'])


def parse_page(response):
    item = BusItem()
    sel = Selector(response)

    name = sel.xpath('//*[@id="bus_line"]/div[1]/div/div/h1/text()').extract()
    item['name'] = str(name[0]).replace("&nbsp", "")

    bus_type = sel.xpath('//*[@id="bus_line"]/div[1]/div/div/a/text()').extract()
    item['bus_type'] = bus_type[0]

    time = sel.xpath('//*[@id="bus_line"]/div[1]/div/p[1]/text()').extract()
    item['time'] = time[0]

    cost = sel.xpath('//*[@id="bus_line"]/div[1]/div/p[2]/text()').extract()
    item['cost'] = cost[0]

    company = sel.xpath('//*[@id="bus_line"]/div[1]/div/p[3]/a/text()').extract()
    item['company'] = company[0]

    update_time = sel.xpath('//*[@id="bus_line"]/div[1]/div/p[4]/text()').extract()
    item['update_time'] = update_time[0]

    line_name = sel.xpath('//*[@class="bus_line_txt"]/strong/text()').extract()
    line_info = sel.xpath('//*[@class="bus_site_layer"]')
    if len(line_name) >= 1:
        item['first_name'] = line_name[0]
        item['first_line'] = parse_aline(line_info[0])
        if len(line_name) >= 2:
            item['second_name'] = line_name[1]
            item['second_line'] = parse_aline(line_info[1])
        else:
            item['second_name'] = ""
            item['second_line'] = ""
    else:
        item['first_name'] = ""
        item['first_line'] = ""

    # print_item(item)
    print(item['name'])
    yield item


class BusSpider(CrawlSpider):
    name = 'bus_spi'
    start_urls = ['https://shenzhen.8684.cn/line7']

    def parse(self, response):
        # print(response.url)
        sel = Selector(response)
        divs = sel.xpath('//*[@id="con_site_1"]/a')
        for dd in divs:
            # print(dd)
            url_back = dd.xpath('@href').extract()
            url = 'https://shenzhen.8684.cn' + url_back[0]
            yield Request(url, callback=parse_page)
