import os
from os.path import normpath
from urllib.parse import parse_qs, urlparse

import scrapy
from lxml import etree
from scrapy.crawler import CrawlerProcess

BASE = os.path.dirname(__file__)

DATA_DIR = os.path.join(BASE, "data")
JOB_DIR = os.path.join(BASE, ".scrapy")


class Spider(scrapy.Spider):
    # See https://github.com/fbbs/fbbs/blob/master/fcgi/bbsann.c
    name = "fudan"
    allowed_domains = ["bbs.fudan.edu.cn"]
    start_urls = [
        "https://bbs.fudan.edu.cn/bbs/0an?path=/groups/rec.faq/ANSI/",
    ]

    def parse(self, response, **_):
        url_parts = urlparse(response.url)
        bbs_path = parse_qs(url_parts.query)["path"][0]  # noqa

        dirname = os.path.join(DATA_DIR, bbs_path.lstrip("/"))
        os.makedirs(dirname, exist_ok=True)

        filename = os.path.join(dirname, ".index.xml")
        with open(filename, "wb") as fp:
            fp.write(response.body)

        root = etree.fromstring(response.body)

        links = root.xpath("//ent")
        for link in links:
            link_path = bbs_path + link.get("path")
            link_path = normpath(link_path)

            if link.get("t") == "f":
                # It's a file
                url = f"https://bbs.fudan.edu.cn/bbs/anc?path={link_path}"  # noqa
                yield response.follow(url, self.parse_anc)
            elif link.get("t") == "d":
                # It's a directory
                url = f"https://bbs.fudan.edu.cn/bbs/0an?path={link_path}"  # noqa
                yield response.follow(url, self.parse)
            else:
                # It's an error
                pass

    def parse_anc(self, response, **_):
        url_parts = urlparse(response.url)
        bbs_path = parse_qs(url_parts.query)["path"][0]  # noqa

        filename = f"data/{bbs_path.lstrip('/')}.xml"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "wb") as fp:
            fp.write(response.body)


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "DOWNLOAD_DELAY": 1.0,
            "JOBDIR": JOB_DIR,
        }
    )
    process.crawl(Spider)
    process.start()
