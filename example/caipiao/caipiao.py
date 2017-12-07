#coding=utf-8

from xspider.spider.spider import BaseSpider
from xspider.filters import UrlFilter
from xspider.processor import PageProcessor
from xspider.selector import XPathSelector
from xspider.filters.CrawledFilter import SimpleCrawledFilter
from xspider.pipeline import FilePipeLine
from xspider import model
from b2 import system2
system2.reload_utf8()

#http://kaijiang.500.com/shtml/ssq/17143.shtml


class KaiJiang(PageProcessor.PageProcessor):
    def __init__(self):
        super(KaiJiang, self).__init__()
        self.title_extractor = XPathSelector.XpathSelector(
            path="//title/text()")
        self.fahao_extractor = XPathSelector.XpathSelector(
            path=
            "//table[@class='kj_tablelist02'][1]/tr[2]/td/table/tr[2]/td[2]/text()"
        )

    def process(self, page, spider):
        items = model.fileds.Fileds()
        items["url"] = page.url
        items["qishu"] = page.url.split("/")[-1].split(".")[0]
        fahao = self.fahao_extractor.find(page)
        if fahao:
            items["faqiu"] = self.fahao_extractor.find(page).strip()
        return items


if __name__ == "__main__":
    start_url_filter = UrlFilter.UrlStartFilter(
        "http://kaijiang.500.com/shtml/ssq/")
    start_url_filter.set_must_check()
    url_filters = [start_url_filter]
    spider = BaseSpider(
        name="kaijiang",
        url_filters=url_filters,
        crawled_filter=SimpleCrawledFilter(),
        page_processor=KaiJiang(),
        pipeline=[FilePipeLine.DumpFilePipe()],
        allow_site=["kaijiang.500.com"],
        start_urls=["http://kaijiang.500.com/shtml/ssq/17143.shtml"])
    spider.start()
