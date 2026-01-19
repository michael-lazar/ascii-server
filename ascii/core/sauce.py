"""
SAUCE (Standard Architecture for Universal Comment Extensions) encoder/decoder.

This module provides utilities for parsing and writing SAUCE metadata from/to files.

Reference: https://www.acid.org/info/sauce/sauce.htm

This implementation was adapted from: https://github.com/blocktronics/moebius
    (Copyright 2022 Andy Herbert Apache license, version 2.0)
"""

import struct
from enum import IntEnum
from typing import TypedDict

EOF = 26


class DataType(IntEnum):
    NONE = 0
    CHARACTER = 1
    BITMAP = 2
    VECTOR = 3
    AUDIO = 4
    BINARYTEXT = 5
    XBIN = 6
    ARCHIVE = 7
    EXECUTABLE = 8


class FileType(IntEnum):
    NONE = 0
    ASCII = 1
    ANS = 1
    ANSI = 2
    ANSIMATION = 3
    RIPSCRIPT = 4
    PCBOARD = 5
    AVATAR = 6
    HTML = 7
    SOURCE = 8


class LetterSpacing(IntEnum):
    LEGACY = 0
    EIGHT = 1
    NINE = 2


class AspectRatio(IntEnum):
    LEGACY = 0
    STRETCH = 1
    SQUARE = 2


class SauceData(TypedDict):
    columns: int
    rows: int
    title: str
    author: str
    group: str
    date: str
    filesize: int
    data_type: DataType
    file_type: FileType
    ice_colors: bool
    letter_spacing: LetterSpacing
    aspect_ratio: AspectRatio
    font_name: str
    comments: str


def _pad_string(text: str, length: int) -> bytes:
    """Pad string to specified length with spaces (ASCII 32), encode as UTF-8."""
    text_bytes = text.encode("utf-8")
    text_bytes = text_bytes[:length]
    return text_bytes.ljust(length)


def _read_string(data: bytes, offset: int, length: int) -> str:
    """Read and decode string from bytes, strip trailing spaces/nulls."""
    slice_data = data[offset : offset + length]
    return slice_data.decode("utf-8").rstrip(" \x00")


def _encode_comments(comments: str) -> list[bytes]:
    """Split the comment string into 64-byte lines."""
    buffer: list[bytes] = []

    if not comments:
        return buffer

    for line in comments.split("\n"):
        line = line.rstrip()
        line_bytes = line.encode("utf-8")
        while line_bytes:
            # Split a line into multiple lines if it overflows
            chunk, line_bytes = line_bytes[:64], line_bytes[64:]
            buffer.append(chunk.ljust(64))

    return buffer


def _decode_comments(file_bytes: bytes, num_lines: int, sauce_offset: int) -> str:
    """Decode comments from bytes, join lines with newlines."""
    if num_lines == 0:
        return ""

    comment_start = sauce_offset - num_lines * 64
    comment_data = file_bytes[comment_start:sauce_offset]

    lines = []
    for i in range(num_lines):
        chunk = comment_data[i * 64 : (i + 1) * 64]
        line = chunk.decode("utf-8").rstrip()
        lines.append(line)

    return "\n".join(lines)


def strip_sauce(file_bytes: bytes) -> bytes:
    """Strip any existing SAUCE metadata from file bytes."""
    if len(file_bytes) < 128:
        return file_bytes

    sauce_bytes = file_bytes[-128:]
    if sauce_bytes[:7] != b"SAUCE00":
        return file_bytes

    num_comments = sauce_bytes[104]
    sauce_size = 128 + (num_comments * 64 + 5 if num_comments else 0)

    stripped = file_bytes[:-sauce_size]

    # Strip EOF marker (byte 26) if present
    if stripped and stripped[-1] == EOF:
        stripped = stripped[:-1]

    return stripped


def get_sauce(file_bytes: bytes) -> SauceData | None:
    """Parse SAUCE metadata from file bytes."""
    if len(file_bytes) < 128:
        return None

    sauce_bytes = file_bytes[-128:]

    if sauce_bytes[:7] != b"SAUCE00":
        return None

    title = _read_string(sauce_bytes, 7, 35)
    author = _read_string(sauce_bytes, 42, 20)
    group = _read_string(sauce_bytes, 62, 20)
    date = _read_string(sauce_bytes, 82, 8)

    filesize = struct.unpack("<I", sauce_bytes[90:94])[0]
    datatype = DataType(sauce_bytes[94])
    filetype = FileType(sauce_bytes[95])

    if datatype == DataType.BINARYTEXT:
        # The BinaryText datatype does not have a file type, instead the FileType field is used to
        # encode the width of the image.
        columns = filetype * 2
        if filesize > 0:
            rows = filesize // columns // 2
        else:
            rows = 0
    else:
        columns = struct.unpack("<H", sauce_bytes[96:98])[0]
        rows = struct.unpack("<H", sauce_bytes[98:100])[0]

    num_comments = sauce_bytes[104]

    flags = sauce_bytes[105]
    ice_colors = bool(flags & 0x01)
    letter_spacing = LetterSpacing((flags >> 1) & 0b11)
    aspect_ratio = AspectRatio((flags >> 3) & 0b11)

    font_name = _read_string(sauce_bytes, 106, 22)

    sauce_offset = len(file_bytes) - 128
    comments = _decode_comments(file_bytes, num_comments, sauce_offset)

    if filesize == 0:
        filesize = len(file_bytes) - 128
        if num_comments:
            filesize -= num_comments * 64 + 5

    return SauceData(
        columns=columns,
        rows=rows,
        title=title,
        author=author,
        group=group,
        date=date,
        filesize=filesize,
        data_type=datatype,
        file_type=filetype,
        ice_colors=ice_colors,
        letter_spacing=letter_spacing,
        aspect_ratio=aspect_ratio,
        font_name=font_name,
        comments=comments,
    )


def write_sauce(file_bytes: bytes, sauce: SauceData) -> bytes:
    """
    Write SAUCE metadata to file bytes.

    Returns new bytes with SAUCE appended.
    """
    # Strip any existing SAUCE data from the file first
    file_bytes = strip_sauce(file_bytes)

    sauce_block = bytearray(128)

    sauce_block[0:7] = b"SAUCE00"
    sauce_block[7:42] = _pad_string(sauce["title"], 35)
    sauce_block[42:62] = _pad_string(sauce["author"], 20)
    sauce_block[62:82] = _pad_string(sauce["group"], 20)
    sauce_block[82:90] = _pad_string(sauce["date"], 8)

    struct.pack_into("<I", sauce_block, 90, len(file_bytes))

    sauce_block[94] = sauce["data_type"]

    columns = sauce["columns"]
    rows = sauce["rows"]

    if sauce["data_type"] == DataType.BINARYTEXT:
        sauce_block[95] = columns // 2
    else:
        sauce_block[95] = sauce["file_type"]
        struct.pack_into("<H", sauce_block, 96, columns)
        struct.pack_into("<H", sauce_block, 98, rows)

    comments = sauce.get("comments", "")
    comment_chunks = _encode_comments(comments)
    sauce_block[104] = len(comment_chunks)

    if sauce["data_type"] != DataType.XBIN:
        flags = 0
        flags |= (1 if sauce["ice_colors"] else 0) << 0
        flags |= (sauce["letter_spacing"] & 0b11) << 1
        flags |= (sauce["aspect_ratio"] & 0b11) << 3
        sauce_block[105] = flags

        font_name = sauce["font_name"]
        if font_name:
            font_bytes = _pad_string(font_name, 22)
            sauce_block[106:128] = font_bytes

    result = bytearray(file_bytes)
    result.append(EOF)

    if comment_chunks:
        comment_bytes = b"COMNT" + b"".join(comment_chunks)
        result.extend(comment_bytes)

    result.extend(sauce_block)

    return bytes(result)
