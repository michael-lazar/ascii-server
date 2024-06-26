import logging
import re
from dataclasses import dataclass
from typing import cast

from django.utils.html import escape
from django.utils.safestring import mark_safe
from stransi import Ansi, SetAttribute, SetColor
from stransi.attribute import Attribute
from stransi.color import ColorRole

from ascii.fudan.constants import DRAWING_CHARACTERS
from ascii.fudan.utils import get_ansi_length

_logger = logging.getLogger(__name__)


class ANSIParser:
    _re_split_spaces = re.compile(r"(\s+|[^ ]+)")
    _re_compress_whitespace = re.compile(r"[ \t]+")

    @dataclass
    class State:
        fg: int = 7
        bg: int = 0
        bold: bool = False
        underline: bool = False
        blink: bool = False

    def __init__(self, text: str):
        self.text = text
        self.ansi = Ansi(text)

    def build_span(self, text, attributes: dict) -> str:
        """
        Build a <span></span> element with the given attributes.
        """
        parts = [f"{name}='{val}'" for name, val in attributes.items()]
        span = f"<span {' '.join(parts)}>{text}</span>"
        return span

    def apply_line_indents(self, text: str) -> str:
        plaintext = self.to_plaintext()

        buffer: list[str] = []
        for text_line, plaintext_line in zip(text.splitlines(), plaintext.splitlines()):
            offset = 0
            for ch in plaintext_line:
                if ch == " ":
                    offset += 1
                elif ch in DRAWING_CHARACTERS:
                    offset += get_ansi_length(ch)
                else:
                    break

            buffer.append(" " * offset + text_line)

        return "\n".join(buffer)

    def to_plaintext(self) -> str:
        return "".join(part for part in self.ansi.instructions() if isinstance(part, str))

    def to_stripped_text(self) -> str:
        text = self.to_plaintext()
        text = "".join(" " if ch in DRAWING_CHARACTERS else ch for ch in text)
        text = self._re_compress_whitespace.sub(" ", text)
        text = "\n".join(line.strip() for line in text.splitlines())
        return text

    def to_html(self) -> str:
        state = self.State()
        buffer = ""

        for instruction in self.ansi.instructions():
            if isinstance(instruction, str):

                classes: list[str] = []
                style_props: list[str] = []
                attributes: dict[str, str] = {}

                if state.blink:
                    # Blink should apply to all characters EXCEPT spaces (" ").
                    # So we need to split the string up and selectively wrap
                    # non-empty segments with blink tags.
                    inner = ""
                    for seg in self._re_split_spaces.findall(instruction):
                        if seg[0] == " ":
                            inner += seg
                        else:
                            inner += self.build_span(escape(seg), {"class": "blink"})
                else:
                    inner = escape(instruction)

                if state.bold:
                    fg = state.fg + 8
                else:
                    fg = state.fg

                if fg != self.State.fg:
                    style_props.append(f"color: var(--c{fg})")
                if state.bg != self.State.bg:
                    style_props.append(f"background-color: var(--c{state.bg})")

                if state.underline:
                    classes.append("underline")

                if style_props:
                    attributes["style"] = "; ".join(style_props)
                if classes:
                    attributes["class"] = " ".join(classes)

                buffer += self.build_span(inner, attributes)

            elif isinstance(instruction, SetColor):

                code = cast(int, instruction.color.code)  # noqa
                if code < 8:
                    match instruction.role:
                        case ColorRole.FOREGROUND:
                            state.fg = code
                        case ColorRole.BACKGROUND:
                            state.bg = code
                        case _:
                            raise ValueError
                else:
                    _logger.warning(f"Unhandled ANSI: {instruction}")

            elif isinstance(instruction, SetAttribute):

                match instruction.attribute:
                    case Attribute.NORMAL:
                        state = self.State()
                    case Attribute.BOLD:
                        state.bold = True
                    case Attribute.UNDERLINE:
                        state.underline = True
                    case Attribute.NOT_UNDERLINE:
                        state.underline = False
                    case Attribute.BLINK:
                        state.blink = True
                    case _:
                        _logger.warning(f"Unhandled ANSI: {instruction}")

            else:
                _logger.warning(f"Unhandled ANSI: {instruction}")

        return mark_safe(buffer)
