import glob
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from ascii.fudan.models import Document, Menu, MenuLink, MenuLinkType
from ascii.fudan.utils import parse_xml, parse_xml_re, unescape_xml_bytes, unescape_xml_text

DATA_PATH = os.path.join(settings.DATA_ROOT, "spiders", "fudan")


class Command(BaseCommand):
    help = "Import fudan crawl data into the database"

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

        # Populate the foreign-key relationships between the links
        for link in MenuLink.objects.all():
            self.stdout.write(link.path)
            match link.type:
                case MenuLinkType.DIRECTORY:
                    link.target_menu = Menu.objects.filter(path=link.path).first()
                    link.save(update_fields=["target_menu"])
                case MenuLinkType.FILE:
                    link.target_document = Document.objects.filter(path=link.path).first()
                    link.save(update_fields=["target_document"])
                case _:
                    pass

    def ingest_menu(self, filepath: str) -> Menu:
        """
        Ingest a BBS menu file (i.e. announcement).
        """
        with open(filepath, "rb") as fp:
            data = fp.read()

        bbs_path = os.path.relpath(filepath, DATA_PATH)
        bbs_path = "/" + os.path.dirname(bbs_path)

        root = parse_xml(data)
        menu = Menu.objects.create(path=bbs_path)

        menu_links: list[MenuLink] = []

        for order, ent in enumerate(root.findall(".//ent"), start=1):
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

        # Attempt to undo string trimming and add back leading indents.
        if any(">>" in link.text for link in menu_links):
            for link in menu_links:
                if ">>" not in link.text:
                    link.text = " " * 5 + link.text

        MenuLink.objects.bulk_create(menu_links)

        return menu

    def ingest_document(self, filepath: str) -> Document:
        """
        Ingest a BBS document file.
        """
        with open(filepath, "rb") as fp:
            data = fp.read()

        bbs_path = os.path.relpath(filepath, DATA_PATH)
        bbs_path = "/" + os.path.splitext(bbs_path)[0]

        data = parse_xml_re(data)
        data = unescape_xml_bytes(data)

        text = data.decode("gb18030", errors="replace")

        document = Document.objects.create(
            path=bbs_path,
            data=data,
            text=text,
        )

        return document
