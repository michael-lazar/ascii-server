from __future__ import annotations

import logging
import typing
from datetime import date, datetime

from django.utils.functional import cached_property
from stransi import Ansi, SetColor

from ascii.core.sauce import SauceData
from ascii.textmode.choices import (
    ARCHIVE_FILETYPES,
    AUDIO_FILETYPES,
    BITMAP_FILETYPES,
    CHARACTER_FILETYPES,
    VECTOR_FILETYPES,
    AspectRatio,
    DataType,
    FileType,
    LetterSpacing,
)

if typing.TYPE_CHECKING:
    from ascii.textmode.models import ArtFile

_logger = logging.getLogger(__name__)


class ANSIFileInspector:
    def __init__(self, artfile: ArtFile):
        self.artfile = artfile

        with self.artfile.raw_file.open("rb") as fp:
            self.ansi = Ansi(fp.read().decode("cp437", errors="ignore"))

    def get_colors(self) -> list[int]:
        colors: set[int] = set()

        for instruction in self.ansi.instructions():
            if isinstance(instruction, SetColor):
                if instruction.color:
                    code = instruction.color.code  # noqa
                    if code < 8:
                        colors.add(code)

        return sorted(colors)


class Sauce:
    """
    https://www.acid.org/info/sauce/sauce.htm
    """

    def __init__(self, data: dict | SauceData):
        self.data = data

    @property
    def title(self) -> str:
        return self.data.get("Title", "")

    @property
    def author(self) -> str:
        return self.data.get("Author", "")

    @property
    def group(self) -> str:
        return self.data.get("Group", "")

    @property
    def comments(self) -> str:
        return self.data.get("Comments", "")

    @property
    def date(self) -> date | None:
        if "Date" not in self.data:
            return None

        date_str = str(self.data["Date"])
        if not date_str:
            return None

        try:
            return datetime.strptime(date_str, "%Y%m%d").date()
        except Exception:
            _logger.warning(f"Invalid date: {date_str}")
            return None

    @cached_property
    def datatype(self) -> DataType | None:
        datatype = self.data.get("Datatype")
        if datatype is None:
            return None

        return DataType(datatype)

    @cached_property
    def filetype(self) -> FileType | None:
        if self.datatype is None:
            return None

        filetype = self.data.get("Filetype")
        if filetype is None:
            return None

        try:
            match self.datatype:
                case DataType.NONE:
                    return FileType.NONE
                case DataType.CHARACTER:
                    return CHARACTER_FILETYPES[filetype]
                case DataType.BITMAP:
                    return BITMAP_FILETYPES[filetype]
                case DataType.VECTOR:
                    return VECTOR_FILETYPES[filetype]
                case DataType.AUDIO:
                    return AUDIO_FILETYPES[filetype]
                case DataType.BINARYTEXT:
                    return FileType.BINARYTEXT
                case DataType.XBIN:
                    return FileType.XBIN
                case DataType.ARCHIVE:
                    return ARCHIVE_FILETYPES[filetype]
                case DataType.EXECUTABLE:
                    return FileType.EXECUTABLE
                case _:
                    return FileType.NONE
        except IndexError:
            _logger.warning(f"Invalid filetype: {filetype}")
            return None

    @property
    def pixel_width(self) -> int | None:
        if self.datatype == DataType.BITMAP or self.filetype == FileType.RIPSCRIPT:
            return self.data.get("Tinfo1")

        return None

    @property
    def pixel_height(self) -> int | None:
        if self.datatype == DataType.BITMAP or self.filetype == FileType.RIPSCRIPT:
            return self.data.get("Tinfo2")

        return None

    @property
    def pixel_depth(self) -> int | None:
        if self.datatype == DataType.BITMAP:
            return self.data.get("Tinfo3")

        return None

    @property
    def sample_rate(self) -> int | None:
        if self.filetype in (
            FileType.SMP8,
            FileType.SMP16,
            FileType.SMP8S,
            FileType.SMP16S,
        ):
            return self.data.get("Tinfo1")

        return None

    @property
    def character_width(self) -> int | None:
        if self.filetype in (
            FileType.ASCII,
            FileType.ANSI,
            FileType.ANSIMATION,
            FileType.PCBOARD,
            FileType.AVATAR,
            FileType.TUNDRADRAW,
            FileType.XBIN,
        ):
            return self.data.get("Tinfo1")

        return None

    @property
    def number_of_lines(self) -> int | None:
        if self.filetype in (
            FileType.ASCII,
            FileType.ANSI,
            FileType.ANSIMATION,
            FileType.PCBOARD,
            FileType.AVATAR,
            FileType.TUNDRADRAW,
            FileType.XBIN,
        ):
            return self.data.get("Tinfo2")

        return None

    @property
    def font_name(self) -> str:
        if self.filetype in (
            FileType.ASCII,
            FileType.ANSI,
            FileType.ANSIMATION,
            FileType.XBIN,
        ):
            return self.data.get("Tinfos", "")

        return ""

    @property
    def filesize(self) -> int:
        return self.data.get("Filesize", 0)

    @property
    def ice_colors(self) -> bool | None:
        ice_colors = self.data.get("ansiflags", {}).get("blink", None)
        if ice_colors is not None:
            return bool(ice_colors)

        return None

    @property
    def letter_spacing(self) -> LetterSpacing | None:
        ls = self.data.get("ansiflags", {}).get("ls", None)
        if ls is not None:
            return LetterSpacing(ls)

        return None

    @property
    def aspect_ratio(self) -> AspectRatio | None:
        ar = self.data.get("ansiflags", {}).get("ar", None)
        if ar is not None:
            return AspectRatio(ar)

        return None
