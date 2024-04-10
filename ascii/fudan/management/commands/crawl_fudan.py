import os
from os.path import normpath
from urllib.parse import parse_qs, urlparse

import scrapy
from django.conf import settings
from django.core.management.base import BaseCommand
from lxml import etree
from scrapy.crawler import CrawlerProcess

BASE_URL = "https://bbs.fudan.edu.cn/bbs"
DATA_PATH = os.path.join(settings.DATA_ROOT, "spiders", "fudan")


class Spider(scrapy.Spider):
    # See https://github.com/fbbs/fbbs/blob/master/fcgi/bbsann.c for
    # guidance on the structure of the XML responses.

    name = "fudan"
    allowed_domains = ["bbs.fudan.edu.cn"]
    start_urls = [f"{BASE_URL}/0an?path=/groups/rec.faq/ANSI/"]

    def parse(self, response, **_):
        url_parts = urlparse(response.url)
        bbs_path = parse_qs(url_parts.query)["path"][0]  # noqa

        dirname = os.path.join(DATA_PATH, bbs_path.lstrip("/"))
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
                url = f"{BASE_URL}/anc?path={link_path}"  # noqa
                yield response.follow(url, self.parse_anc)
            elif link.get("t") == "d":
                # It's a directory
                url = f"{BASE_URL}/0an?path={link_path}"  # noqa
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


class Command(BaseCommand):
    help = "Crawl fudan essence area"

    def handle(self, *args, **options):
        process = CrawlerProcess(
            settings={
                "DOWNLOAD_DELAY": 1.0,
                "JOBDIR": ".scrapy",
            }
        )
        process.crawl(Spider)
        process.start()
