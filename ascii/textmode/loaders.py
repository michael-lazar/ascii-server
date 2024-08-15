from urllib.parse import quote

from django.core.files.base import ContentFile

from ascii.textmode.clients import SixteenColorsClient
from ascii.textmode.models import ArtFile, ArtistTag, ArtPack, ContentTag, GroupTag


class SixteenColorsPackImporter:
    """
    Import a single art pack and all associated metadata from 16colo.rs.
    """

    def __init__(self, name: str):
        self.name = name
        self.client = SixteenColorsClient()

    def process(self) -> ArtPack:
        data = self.client.get_pack(self.name)

        pack, _ = ArtPack.objects.get_or_create(name=self.name)

        for artfile_name, artfile_data in data["files"].items():
            artist_tags: list[ArtistTag] = []
            for tag_name in artfile_data.get("artists", []):
                tag, _ = ArtistTag.objects.get_or_create(name=tag_name)
                artist_tags.append(tag)

            content_tags: list[ContentTag] = []
            for tag_name in artfile_data.get("content", []):
                tag, _ = ContentTag.objects.get_or_create(name=tag_name)
                content_tags.append(tag)

            group_tags: list[GroupTag] = []
            for tag_name in artfile_data.get("groups", []):
                tag, _ = GroupTag.objects.get_or_create(name=tag_name)
                group_tags.append(tag)

            sauce = artfile_data.get("sauce", {})

            raw_name = artfile_data["file"]["raw"]
            raw_data = self.client.get_file(f"/pack/{self.name}/raw/{quote(raw_name)}")
            raw_file = ContentFile(raw_data, name=raw_name)

            image_tn_name = artfile_data["file"]["tn"]["file"]
            image_tn_data = self.client.get_file(f"/pack/{self.name}/tn/{quote(image_tn_name)}")
            image_tn_file = ContentFile(image_tn_data, name=image_tn_name)

            image_x1_name = artfile_data["file"]["x1"]["file"]
            image_x1_data = self.client.get_file(f"/pack/{self.name}/x1/{quote(image_x1_name)}")
            image_x1_file = ContentFile(image_x1_data, name=image_x1_name)

            if x2_data := artfile_data["file"].get("x2"):
                image_x2_name = x2_data["file"]
                image_x2_data = self.client.get_file(f"/pack/{self.name}/x2/{quote(image_x2_name)}")
                image_x2_file = ContentFile(image_x2_data, name=image_x2_name)
            else:
                image_x2_file = None

            is_fileid = artfile_name == data["fileid"]

            artfile, _ = ArtFile.objects.update_or_create(
                name=artfile_name,
                pack=pack,
                defaults={
                    "raw": raw_file,
                    "image_tn": image_tn_file,
                    "image_x1": image_x1_file,
                    "image_x2": image_x2_file,
                    "sauce": sauce,
                    "is_fileid": is_fileid,
                },
            )

            artfile.artist_tags.set(artist_tags)
            artfile.content_tags.set(content_tags)
            artfile.group_tags.set(group_tags)

        return pack