import html
import os
import re
import zipfile
from datetime import date

from django.core.management.base import BaseCommand

from ascii.huku.models import MLTDirectory, MLTFile, MLTItem, MLTItemType

DATE_RE = re.compile(r"(\d{4})[/年](\d{1,2})[/月](\d{1,2})")
ENCODING = "cp932"


class Command(BaseCommand):
    help = "Import an MLT-formatted zip archive into the database"

    def add_arguments(self, parser):
        parser.add_argument("zipfile", type=str, help="Path to the .zip archive")

    def handle(self, *args, **options):
        zip_path = options["zipfile"]

        MLTFile.objects.all().delete()
        MLTDirectory.objects.all().delete()
        MLTItem.objects.all().delete()

        with zipfile.ZipFile(zip_path) as zf:
            dir_objs: dict[str, MLTDirectory] = {}

            for zinfo in zf.infolist():
                # filenames in zip files are CP437 encoded by default
                raw_filename = zinfo.filename.encode("cp437")
                filename = raw_filename.decode(ENCODING)

                # Drop the first path segment which is the directory of the ZIP file
                filename = "/" + filename.split("/", maxsplit=1)[1]

                if filename == "/":
                    parent = None
                else:
                    parent_path = os.path.dirname(filename.rstrip("/"))
                    if parent_path != "/":
                        parent_path += "/"
                    parent = dir_objs[parent_path]

                if filename.endswith(".csv"):
                    # These are for bookkeeping the history of the archive
                    continue

                if zinfo.is_dir():
                    dir_objs[filename] = MLTDirectory.objects.create(
                        path=filename,
                        name=os.path.basename(filename.rstrip("/")),
                        parent=parent,
                    )
                    self.stdout.write(f"Imported {filename}")
                    continue

                if not filename.lower().endswith(".mlt"):
                    self.stderr.write(f"Skipping unknown file type: {filename}")
                    continue

                with zf.open(zinfo) as fp:
                    raw_data = fp.read()

                decoding_error = False
                try:
                    text = raw_data.decode(ENCODING)
                except UnicodeDecodeError:
                    text = raw_data.decode(ENCODING, errors="replace")
                    decoding_error = True

                # For whatever reason some of the files have HTML escape sequences in them.
                text = html.unescape(text)

                parts = text.split("\r\n[SPLIT]")

                # Sometimes the file is broken and starts with an extra [SPLIT]
                while not parts[0]:
                    parts = parts[1:]

                last_update: date | None = None
                if m := DATE_RE.search(parts[0]):
                    try:
                        last_update = date(*map(int, m.groups()))
                    except ValueError:
                        self.stdout.write(f"Failed to parse date: {parts[0]}")

                base_name = os.path.splitext(os.path.basename(filename))[0]
                mlt_file = MLTFile.objects.create(
                    parent=parent,
                    path=filename[:-4],  # Drop the .mlt
                    name=base_name,
                    last_update=last_update,
                    data=raw_data,
                    decoding_error=decoding_error,
                )

                artwork_count = 0
                nsfw = "R18" in base_name
                for order, part in enumerate(parts[1:]):
                    lines = part.strip().splitlines()
                    line_count = len(lines)

                    if line_count == 1:
                        heading = lines[0].strip()
                        MLTItem.objects.create(
                            mlt_file=mlt_file,
                            item_type=MLTItemType.HEADING,
                            order=order,
                            heading=heading,
                            line_count=line_count,
                        )
                        if "R18" in heading:
                            nsfw = True

                    else:
                        text = part.lstrip("\r\n")
                        text = "\n".join(line for line in text.splitlines())

                        MLTItem.objects.create(
                            mlt_file=mlt_file,
                            item_type=MLTItemType.ARTWORK,
                            order=order,
                            text=text,
                            line_count=line_count,
                        )
                        artwork_count += 1

                mlt_file.artwork_count = artwork_count
                mlt_file.nsfw = nsfw
                mlt_file.save(update_fields=["artwork_count", "nsfw"])

                self.stdout.write(f"Imported {filename}")

        self.stdout.write(self.style.SUCCESS("ZIP import complete"))
