from urllib.parse import quote

from django.core.files.base import ContentFile

from ascii.textmode.choices import TagCategory
from ascii.textmode.clients import SixteenColorsClient
from ascii.textmode.models import ArtFile, ArtFileTag, ArtPack
from ascii.textmode.sauce import Sauce


class SixteenColorsPackImporter:
    """
    Import a single art pack and all associated metadata from 16colo.rs.
    """

    def __init__(self, name: str, year: int):
        self.name = name
        self.year = year
        self.client = SixteenColorsClient()

    def process(self) -> ArtPack:
        data = self.client.get_pack(self.name)

        ArtPack.objects.filter(name=self.name).delete()

        zip_name = f"{self.name}.zip"
        zip_data = self.client.get_file(f"/archive/{self.year}/{zip_name}")
        zip_file = ContentFile(zip_data, name=zip_name)

        pack = ArtPack.objects.create(name=self.name, year=self.year, zip_file=zip_file)

        for artfile_name, artfile_data in data["files"].items():

            tags: list[ArtFileTag] = []

            for tag_name in artfile_data.get("artists", []):
                tag, _ = ArtFileTag.objects.get_or_create(
                    category=TagCategory.ARTIST,
                    name=tag_name,
                )
                tags.append(tag)

            for tag_name in artfile_data.get("content", []):
                tag, _ = ArtFileTag.objects.get_or_create(
                    category=TagCategory.CONTENT,
                    name=tag_name,
                )
                tags.append(tag)

            for tag_name in artfile_data.get("groups", []):
                tag, _ = ArtFileTag.objects.get_or_create(
                    category=TagCategory.GROUP,
                    name=tag_name,
                )
                tags.append(tag)

            sauce = Sauce(artfile_data.get("sauce", {}))

            raw_name = artfile_data["file"]["raw"]
            raw_data = self.client.get_file(f"/pack/{self.name}/raw/{quote(raw_name)}")
            raw_file = ContentFile(raw_data, name=raw_name)

            if "tn" in artfile_data["file"]:
                image_tn_name = artfile_data["file"]["tn"]["file"]
                image_tn_data = self.client.get_file(f"/pack/{self.name}/tn/{quote(image_tn_name)}")
                image_tn_file = ContentFile(image_tn_data, name=image_tn_name)
            else:
                image_tn_file = None

            if "x1" in artfile_data["file"]:
                image_x1_name = artfile_data["file"]["x1"]["file"]
                image_x1_data = self.client.get_file(f"/pack/{self.name}/x1/{quote(image_x1_name)}")
                image_x1_file = ContentFile(image_x1_data, name=image_x1_name)
            else:
                image_x1_file = None

            if "x2" in artfile_data["file"]:
                image_x2_name = artfile_data["file"]["x2"]["file"]
                image_x2_data = self.client.get_file(f"/pack/{self.name}/x2/{quote(image_x2_name)}")
                image_x2_file = ContentFile(image_x2_data, name=image_x2_name)
            else:
                image_x2_file = None

            is_fileid = artfile_name == data["fileid"]

            artfile = ArtFile.objects.create(
                name=artfile_name,
                pack=pack,
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
                datatype=sauce.datatype,
                filetype=sauce.filetype,
                pixel_width=sauce.pixel_width,
                pixel_height=sauce.pixel_height,
                character_width=sauce.character_width,
                number_of_lines=sauce.number_of_lines,
                ice_colors=sauce.ice_colors,
                letter_spacing=sauce.letter_spacing,
            )

            artfile.tags.set(tags)

        return pack
