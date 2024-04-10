import glob
import os
import re
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from ascii.fundan.models import Document, Menu, MenuLink
from ascii.fundan.utils import parse_xml, parse_xml_re, unescape_xml_bytes, unescape_xml_text

DATA_PATH = os.path.join(settings.DATA_ROOT, "spiders", "fundan")


class Command(BaseCommand):
    help = "Import fundan crawl data into the database"

    xml_document_pattern = re.compile(rb"<po>(.*?)</po>", re.DOTALL)

    def handle(self, *args, **options):

        Menu.objects.all().delete()

        pattern = os.path.join(DATA_PATH, "**", ".index.xml")
        for filepath in glob.glob(pattern, recursive=True):
            self.stdout.write(filepath)
            self.ingest_menu(filepath)

        Document.objects.all().delete()

        pattern = os.path.join(DATA_PATH, "**", "*.xml")
        for filepath in glob.glob(pattern, recursive=True):
            self.stdout.write(filepath)
            self.ingest_document(filepath)

    def ingest_menu(self, filepath: str) -> Menu:
        """
        Ingest a BBS menu file (i.e. announcement).
        """
        with open(filepath, "rb") as fp:
            data = fp.read()

        bbs_path = "/" + os.path.relpath(filepath, DATA_PATH)
        bbs_path = os.path.dirname(bbs_path)

        root = parse_xml(data)
        menu = Menu.objects.create(path=bbs_path)

        menu_links: list[MenuLink] = []

        for order, ent in enumerate(root.findall(".//ent")):
            ent_path = os.path.normpath(bbs_path + ent.get("path"))
            ent_time = datetime.fromisoformat(ent.get("time"))
            ent_time = timezone.make_aware(ent_time, timezone.utc)
            ent_type = ent.get("t")
            ent_organizer = ent.get("id") or ""
            ent_text = unescape_xml_text(ent.text or "")

            menu_links.append(
                MenuLink(
                    menu=menu,
                    order=order,
                    organizer=ent_organizer,
                    path=ent_path,
                    time=ent_time,
                    type=ent_type,
                    text=ent_text,
                )
            )

        MenuLink.objects.bulk_create(menu_links)

        return menu

    def ingest_document(self, filepath: str) -> Document:
        """
        Ingest a BBS document file.
        """
        with open(filepath, "rb") as fp:
            data = fp.read()

        bbs_path = "/" + os.path.relpath(filepath, DATA_PATH)
        bbs_path, _ = os.path.splitext(bbs_path)

        data = parse_xml_re(data)
        data = unescape_xml_bytes(data)

        document = Document.objects.create(
            path=bbs_path,
            data=data,
            html="",
        )

        return document
