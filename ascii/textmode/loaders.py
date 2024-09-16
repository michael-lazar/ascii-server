import logging
from urllib.parse import quote

from django.core.files.base import ContentFile

from ascii.textmode.choices import TagCategory
from ascii.textmode.clients import SixteenColorsClient
from ascii.textmode.models import ArtFile, ArtFileTag, ArtPack
from ascii.textmode.sauce import Sauce

_logger = logging.getLogger(__name__)


class SixteenColorsPackImporter:
    """
    Import a single art pack and all associated metadata from 16colo.rs.
    """

    fileid: str
    year: int
    pack: ArtPack

    def __init__(self, name: str):
        self.name = name
        self.client = SixteenColorsClient()

    def process(self) -> ArtPack:
        data = self.client.get_pack(self.name)

        self.year = data["year"]
        self.fileid = data["fileid"]

        def get_zip_file():
            zip_name = f"{self.name}.zip"
            zip_data = self.client.get_file(f"/archive/{self.year}/{zip_name}")
            return ContentFile(zip_data, name=zip_name)

        self.pack, _ = ArtPack.objects.get_or_create(
            name=self.name,
            defaults={
                "year": self.year,
                "zip_file": get_zip_file,
            },
        )

        for artfile_name, artfile_data in data["files"].items():
            try:
                self.process_file(artfile_name, artfile_data)
            except Exception as e:
                _logger.warning(
                    f"Failed to process file: {artfile_name}, {artfile_data}",
                    exc_info=e,
                )

        return self.pack

    def process_file(self, name, data):

        sauce = Sauce(data.get("sauce", {}))

        defaults = {
            "sauce_data": sauce.data,
            "is_fileid": name == self.fileid,
            "title": sauce.title,
            "author": sauce.author,
            "group": sauce.group,
            "date": sauce.date,
            "comments": sauce.comments,
            "datatype": sauce.datatype,
            "filetype": sauce.filetype,
            "pixel_width": sauce.pixel_width,
            "pixel_height": sauce.pixel_height,
            "character_width": sauce.character_width,
            "number_of_lines": sauce.number_of_lines,
            "ice_colors": sauce.ice_colors,
            "letter_spacing": sauce.letter_spacing,
            "font_name": sauce.font_name,
            "aspect_ratio": sauce.aspect_ratio,
        }

        def get_raw_file():
            raw_name = data["file"]["raw"]
            raw_data = self.client.get_file(f"/pack/{self.name}/raw/{quote(raw_name)}")
            return ContentFile(raw_data, name=raw_name)

        def get_image_tn():
            if "tn" not in data["file"]:
                return None

            image_tn_name = data["file"]["tn"]["file"]
            image_tn_data = self.client.get_file(f"/pack/{self.name}/tn/{quote(image_tn_name)}")
            return ContentFile(image_tn_data, name=image_tn_name)

        def get_image_x1():
            if "x1" not in data["file"]:
                return None

            image_x1_name = data["file"]["x1"]["file"]
            image_x1_data = self.client.get_file(f"/pack/{self.name}/x1/{quote(image_x1_name)}")
            return ContentFile(image_x1_data, name=image_x1_name)

        create_defaults = {
            **defaults,
            "raw_file": get_raw_file,
            "image_tn": get_image_tn,
            "image_x1": get_image_x1,
        }

        artfile, _ = ArtFile.objects.update_or_create(
            defaults=defaults,
            create_defaults=create_defaults,
            name=name,
            pack=self.pack,
        )

        tags: list[ArtFileTag] = []
        for tag_name in data.get("artists", []):
            tag, _ = ArtFileTag.objects.get_or_create(category=TagCategory.ARTIST, name=tag_name)
            tags.append(tag)
        for tag_name in data.get("content", []):
            tag, _ = ArtFileTag.objects.get_or_create(category=TagCategory.CONTENT, name=tag_name)
            tags.append(tag)
        for tag_name in data.get("groups", []):
            tag, _ = ArtFileTag.objects.get_or_create(category=TagCategory.GROUP, name=tag_name)
            tags.append(tag)

        artfile.tags.set(tags)
