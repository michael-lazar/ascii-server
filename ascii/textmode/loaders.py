import logging
from urllib.parse import quote

import requests
from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile
from django.utils.text import get_valid_filename

from ascii.textmode.choices import TagCategory
from ascii.textmode.clients import PackNotFoundError, SixteenColorsClient
from ascii.textmode.models import ArtFile, ArtFileTag, ArtPack
from ascii.textmode.sauce import Sauce

_logger = logging.getLogger(__name__)

BLACKLIST = [
    "2xl_crew-the_collection",  # 50 MB pack with a directory in it, generally weird
    "openworld-01",  # Empty, broken pack
    "yoda16",  # Empty, broken pack
]

# Packs where the zip filename on the server doesn't match the archive name
# returned by the API.
ZIP_RENAMES = {
    "cn!202101.zip": "cn202101.zip",  # https://github.com/16colo-rs/16c/issues/94
    "ace-r#2.zip": "ace-r2.zip",  # The server strips "#" from archive filenames
    "ace-r#3.zip": "ace-r3.zip",
}


def build_content_file(data: bytes, name: str) -> ContentFile:
    """
    Some historical filenames (e.g. "────────.───") have no characters that
    survive django's filename sanitization, and FileField will refuse to store
    them. Fall back to a percent-encoded ASCII filename; the original name is
    still preserved on the ArtFile.name field.
    """
    try:
        get_valid_filename(name)
    except SuspiciousFileOperation:
        name = quote(name, safe="")

    return ContentFile(data, name=name)


class SixteenColorsPackImporter:
    """
    Import a single art pack and all associated metadata from 16colo.rs.
    """

    fileid: str | None
    year: int
    pack: ArtPack

    def __init__(self, name: str, skip_tags: bool = False, skip_existing: bool = False):
        self.name = name
        self.client = SixteenColorsClient()
        self.skip_tags = skip_tags
        self.skip_existing = skip_existing

    def process(self) -> ArtPack | None:
        if self.name in BLACKLIST:
            _logger.info(f"Skipping blacklisted pack: {self.name}")
            return None

        if self.skip_existing and ArtPack.objects.filter(name=self.name).exists():
            _logger.info(f"Skipping existing pack: {self.name}")
            return None

        try:
            data = self.client.get_pack(self.name)
        except (PackNotFoundError, requests.RequestException) as e:
            _logger.warning(f"Skipping pack with error: {e}")
            return None

        self.year = data["year"]

        # Some packs (particularly pre-1994) have no FILE_ID.DIZ, and the API
        # omits the "fileid" key for them. They are otherwise importable.
        self.fileid = data.get("fileid")

        def get_zip_file():
            zip_name = data["archive"]
            zip_name = ZIP_RENAMES.get(zip_name, zip_name)
            if zip_name.startswith("mist1019"):
                zip_name = "mist1019.zip"

            zip_data = self.client.get_file(f"/archive/{self.year}/{quote(zip_name)}")
            return build_content_file(zip_data, zip_name)

        # Download the zip before calling get_or_create(), so that the sqlite
        # write lock isn't held during the network request. Some packs (e.g.
        # ansipics) have no zip archive on the server.
        pack_defaults: dict = {"year": self.year, "zip_file": None}
        if "archive" in data and not ArtPack.objects.filter(name=self.name).exists():
            try:
                pack_defaults["zip_file"] = get_zip_file()
            except requests.RequestException as e:
                # See https://16colo.rs/pack/fuel27/, returns 403 FORBIDDEN
                _logger.warning(f"Failed to download pack: {self.name=}, {data=}, {e=}")
                return None

        self.pack, _ = ArtPack.objects.get_or_create(name=self.name, defaults=pack_defaults)

        for artfile_name, artfile_data in data["files"].items():
            try:
                self.process_file(artfile_name, artfile_data)
            except Exception as e:
                _logger.warning(
                    f"Failed to process file: {artfile_name=}, {artfile_data=}, {e=}",
                )

        return self.pack

    def process_file(self, name, data):
        is_joint = len(data.get("artists", [])) > 1
        sauce = Sauce(data.get("sauce", {}))

        defaults = {
            "is_fileid": name == self.fileid,
            "is_joint": is_joint,
            **sauce.as_artfile_fields(),
        }

        def get_raw_file():
            raw_name = data["file"]["raw"]
            raw_data = self.client.get_file(f"/pack/{self.name}/raw/{quote(raw_name)}")
            return build_content_file(raw_data, raw_name)

        def get_image_tn():
            if "tn" not in data["file"]:
                return None

            image_tn_name = data["file"]["tn"]["file"]
            image_tn_data = self.client.get_file(f"/pack/{self.name}/tn/{quote(image_tn_name)}")
            return build_content_file(image_tn_data, image_tn_name)

        def get_image_x1():
            if "x1" not in data["file"]:
                return None

            image_x1_name = data["file"]["x1"]["file"]
            image_x1_data = self.client.get_file(f"/pack/{self.name}/x1/{quote(image_x1_name)}")
            return build_content_file(image_x1_data, image_x1_name)

        # Download the files before calling update_or_create(), so that the
        # sqlite write lock isn't held during the network requests.
        create_defaults = dict(defaults)
        if not ArtFile.objects.filter(pack=self.pack, name=name).exists():
            create_defaults["raw_file"] = get_raw_file()
            create_defaults["image_tn"] = get_image_tn()
            create_defaults["image_x1"] = get_image_x1()

        artfile, created = ArtFile.objects.update_or_create(
            defaults=defaults,
            create_defaults=create_defaults,
            name=name,
            pack=self.pack,
        )

        if created and not self.skip_tags:
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

            artfile.tags.set(tags)
