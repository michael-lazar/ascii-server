import base64
import functools
import io
import os

import uharfbuzz as hb
from django.conf import settings
from django.template.loader import render_to_string
from fontTools import subset
from fontTools.ttLib import TTFont

AAHUB_FONT = os.path.join(settings.BASE_DIR, "core", "static", "core", "fonts", "aahub.woff2")


@functools.cache
def load_aahub_font() -> TTFont:
    return subset.load_font(AAHUB_FONT, subset.Options())


@functools.cache
def load_aa_font_harfbuzz() -> tuple[hb.Face, hb.Font]:
    with open(AAHUB_FONT, "rb") as fp:
        font_data = fp.read()

    face = hb.Face(font_data, 0)
    font = hb.Font(face)
    font.scale = (face.upem, face.upem)
    hb.ot_font_set_funcs(font)

    return face, font


def make_subset_woff2(artwork: str) -> str:
    """
    Return a base-64 woff2 that contains *only* ``characters``.
    """
    opts = subset.Options(
        flavor="woff2",
        with_zopfli=True,  # extra gzip optimisation
        desubroutinize=True,  # shrink CFF fonts
        layout_features=["*"],  # keep kerning etc.
    )

    characters = "".join(set(artwork))

    subsetter = subset.Subsetter(opts)
    subsetter.populate(text=characters)

    font = load_aahub_font()
    subsetter.subset(font)

    buffer = io.BytesIO()
    subset.save_font(font, buffer, opts)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def calculate_max_width(artwork: str) -> float:
    """
    Render the font in order to determine the true width of the text after kerning, etc.

    Return the max width of the artwork in font *units*.

        units * font size (px) = width (px)
    """
    face, font = load_aa_font_harfbuzz()

    max_width = 0
    for line in artwork.splitlines():
        if not line:
            continue

        buf = hb.Buffer()
        buf.add_str(line)
        buf.guess_segment_properties()
        hb.shape(font, buf)

        units = sum(pos.x_advance for pos in buf.glyph_positions) / face.upem
        max_width = max(max_width, units)

    return max_width


def render_artwork_svg(text: str) -> str:
    font_size = 16
    line_height = 18

    lines = text.splitlines()
    rows = ((i * line_height + 10, line) for i, line in enumerate(lines, start=1))

    return render_to_string(
        "huku/aa.svg",
        {
            "rows": rows,
            "font_b64": make_subset_woff2(text),
            "font_size": font_size,
            "width": font_size * calculate_max_width(text),
            "line_height": line_height,
            "height": line_height * len(lines) + 20,
        },
    )
