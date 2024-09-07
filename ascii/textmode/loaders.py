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
    pack: ArtPack

    def __init__(self, name: str):
        self.name = name
        self.client = SixteenColorsClient()

    def process(self) -> ArtPack:
        data = self.client.get_pack(self.name)

        ArtPack.objects.filter(name=self.name).delete()

        year = data["year"]

        zip_name = f"{self.name}.zip"
        zip_data = self.client.get_file(f"/archive/{year}/{zip_name}")
        zip_file = ContentFile(zip_data, name=zip_name)

        self.pack = ArtPack.objects.create(name=self.name, year=year, zip_file=zip_file)
        self.fileid = data["fileid"]

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

        tags: list[ArtFileTag] = []

        for tag_name in data.get("artists", []):
            tag, _ = ArtFileTag.objects.get_or_create(
                category=TagCategory.ARTIST,
                name=tag_name,
            )
            tags.append(tag)

        for tag_name in data.get("content", []):
            tag, _ = ArtFileTag.objects.get_or_create(
                category=TagCategory.CONTENT,
                name=tag_name,
            )
            tags.append(tag)

        for tag_name in data.get("groups", []):
            tag, _ = ArtFileTag.objects.get_or_create(
                category=TagCategory.GROUP,
                name=tag_name,
            )
            tags.append(tag)

        sauce = Sauce(data.get("sauce", {}))

        raw_name = data["file"]["raw"]
        raw_data = self.client.get_file(f"/pack/{self.name}/raw/{quote(raw_name)}")
        raw_file = ContentFile(raw_data, name=raw_name)

        if "tn" in data["file"]:
            image_tn_name = data["file"]["tn"]["file"]
            image_tn_data = self.client.get_file(f"/pack/{self.name}/tn/{quote(image_tn_name)}")
            image_tn_file = ContentFile(image_tn_data, name=image_tn_name)
        else:
            image_tn_file = None

        if "x1" in data["file"]:
            image_x1_name = data["file"]["x1"]["file"]
            image_x1_data = self.client.get_file(f"/pack/{self.name}/x1/{quote(image_x1_name)}")
            image_x1_file = ContentFile(image_x1_data, name=image_x1_name)
        else:
            image_x1_file = None

        if "x2" in data["file"]:
            image_x2_name = data["file"]["x2"]["file"]
            image_x2_data = self.client.get_file(f"/pack/{self.name}/x2/{quote(image_x2_name)}")
            image_x2_file = ContentFile(image_x2_data, name=image_x2_name)
        else:
            image_x2_file = None

        is_fileid = name == self.fileid

        artfile = ArtFile.objects.create(
            name=name,
            pack=self.pack,
            raw_file=raw_file,
            image_tn=image_tn_file,
            image_x1=image_x1_file,
            image_x2=image_x2_file,
            sauce_data=sauce.data,
            is_fileid=is_fileid,
            title=sauce.title,
            author=sauce.author,
            group=sauce.group,
            date=sauce.date,
            comments=sauce.comments,
            datatype=sauce.datatype,
            filetype=sauce.filetype,
            pixel_width=sauce.pixel_width,
            pixel_height=sauce.pixel_height,
            character_width=sauce.character_width,
            number_of_lines=sauce.number_of_lines,
            ice_colors=sauce.ice_colors,
            letter_spacing=sauce.letter_spacing,
            font_name=sauce.font_name,
            aspect_ratio=sauce.aspect_ratio,
        )

        artfile.tags.set(tags)
