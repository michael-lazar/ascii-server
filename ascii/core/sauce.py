"""
SAUCE (Standard Architecture for Universal Comment Extensions) encoder/decoder.

This module provides utilities for parsing and writing SAUCE metadata from/to files.

Reference: https://www.acid.org/info/sauce/sauce.htm

This implementation was adapted from: https://github.com/blocktronics/moebius
    (Copyright 2022 Andy Herbert Apache license, version 2.0)
"""

import struct
from typing import TypedDict

EOF = 26


class AnsiFlags(TypedDict):
    blink: int
    ls: int
    ar: int
    ice: int


# This format was copied from the format that 16colo.rs uses in API responses.
class SauceData(TypedDict):
    Id: str
    Version: int
    Title: str
    Author: str
    Group: str
    Date: str
    Filesize: int
    Datatype: int
    Filetype: int
    Tinfo1: int
    Tinfo2: int
    Tinfo3: int
    Tinfo4: int
    Comments: str
    Tflags: int
    Tinfos: str
    ansiflags: AnsiFlags


def _pad_string(text: str, length: int, fillchar: bytes = b" ") -> bytes:
    """Pad string to specified length, encode as UTF-8."""
    text_bytes = text.encode("utf-8")
    text_bytes = text_bytes[:length]
    return text_bytes.ljust(length, fillchar)


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


def get_sauce_data(file_bytes: bytes) -> SauceData | None:
    """Parse SAUCE metadata from file bytes."""
    if len(file_bytes) < 128:
        return None

    sauce_bytes = file_bytes[-128:]

    if sauce_bytes[:7] != b"SAUCE00":
        return None

    version = 0
    title = _read_string(sauce_bytes, 7, 35)
    author = _read_string(sauce_bytes, 42, 20)
    group = _read_string(sauce_bytes, 62, 20)
    date = _read_string(sauce_bytes, 82, 8)

    filesize = struct.unpack("<I", sauce_bytes[90:94])[0]
    datatype = sauce_bytes[94]
    filetype = sauce_bytes[95]

    tinfo1 = struct.unpack("<H", sauce_bytes[96:98])[0]
    tinfo2 = struct.unpack("<H", sauce_bytes[98:100])[0]
    tinfo3 = struct.unpack("<H", sauce_bytes[100:102])[0]
    tinfo4 = struct.unpack("<H", sauce_bytes[102:104])[0]

    num_comments = sauce_bytes[104]
    tflags = sauce_bytes[105]
    tinfos = _read_string(sauce_bytes, 106, 22)

    sauce_offset = len(file_bytes) - 128
    comments = _decode_comments(file_bytes, num_comments, sauce_offset)

    if filesize == 0:
        filesize = len(file_bytes) - 128
        if num_comments:
            filesize -= num_comments * 64 + 5

    # Parse ansiflags from tflags
    blink = tflags & 0x01
    ls = (tflags >> 1) & 0b11
    ar = (tflags >> 3) & 0b11
    ice = blink  # ice and blink are the same

    return SauceData(
        Id="SAUCE",
        Version=version,
        Title=title,
        Author=author,
        Group=group,
        Date=date,
        Filesize=filesize,
        Datatype=datatype,
        Filetype=filetype,
        Tinfo1=tinfo1,
        Tinfo2=tinfo2,
        Tinfo3=tinfo3,
        Tinfo4=tinfo4,
        Comments=comments,
        Tflags=tflags,
        Tinfos=tinfos,
        ansiflags=AnsiFlags(
            blink=blink,
            ls=ls,
            ar=ar,
            ice=ice,
        ),
    )


def write_sauce_data(file_bytes: bytes, sauce: SauceData) -> bytes:
    """
    Write SAUCE metadata to file bytes.

    Returns new bytes with SAUCE appended.
    """
    # Strip any existing SAUCE data from the file first
    file_bytes = strip_sauce(file_bytes)

    sauce_block = bytearray(128)

    sauce_block[0:7] = b"SAUCE00"
    sauce_block[7:42] = _pad_string(sauce["Title"], 35)
    sauce_block[42:62] = _pad_string(sauce["Author"], 20)
    sauce_block[62:82] = _pad_string(sauce["Group"], 20)
    sauce_block[82:90] = _pad_string(sauce["Date"], 8)

    struct.pack_into("<I", sauce_block, 90, len(file_bytes))

    sauce_block[94] = sauce["Datatype"]
    sauce_block[95] = sauce["Filetype"]

    struct.pack_into("<H", sauce_block, 96, sauce["Tinfo1"])
    struct.pack_into("<H", sauce_block, 98, sauce["Tinfo2"])
    struct.pack_into("<H", sauce_block, 100, sauce["Tinfo3"])
    struct.pack_into("<H", sauce_block, 102, sauce["Tinfo4"])

    comments = sauce.get("Comments", "")
    comment_chunks = _encode_comments(comments)
    sauce_block[104] = len(comment_chunks)

    # Build flags from ansiflags
    ansiflags = sauce.get("ansiflags", {})
    blink = ansiflags.get("blink", 0)
    ls = ansiflags.get("ls", 0)
    ar = ansiflags.get("ar", 0)

    flags = 0
    flags |= (blink & 0x01) << 0
    flags |= (ls & 0b11) << 1
    flags |= (ar & 0b11) << 3
    sauce_block[105] = flags

    sauce_block[106:128] = _pad_string(sauce["Tinfos"], 22, fillchar=b"\x00")

    result = bytearray(file_bytes)
    result.append(EOF)

    if comment_chunks:
        comment_bytes = b"COMNT" + b"".join(comment_chunks)
        result.extend(comment_bytes)

    result.extend(sauce_block)

    return bytes(result)
