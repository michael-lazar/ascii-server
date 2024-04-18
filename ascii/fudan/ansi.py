import logging
import re
from dataclasses import dataclass
from typing import cast

from django.utils.html import escape
from django.utils.safestring import mark_safe
from stransi import Ansi, SetAttribute, SetColor
from stransi.attribute import Attribute
from stransi.color import ColorRole

_logger = logging.getLogger(__name__)


DRAWING_CHARACTERS = "─│├┤╭╮╯╰"


class ANSIParser:

    _split_spaces_pattern = re.compile(r"(\s+|[^ ]+)")

    @dataclass
    class State:
        fg: int = 7
        bg: int = 0
        bold: bool = False
        underline: bool = False
        blink: bool = False

    def build_span(self, text: str, attributes: dict) -> str:
        """
        Build a <span></span> element with the given attributes.
        """
        parts = [f"{name}='{val}'" for name, val in attributes.items()]
        span = f"<span {' '.join(parts)}>{text}</span>"
        return span

    def to_plaintext(self, text: str) -> str:
        text = "".join(part for part in Ansi(text).instructions() if isinstance(part, str))
        text = "\n".join(line.strip() for line in text.splitlines())
        text = re.sub("[ \t]+", " ", text)
        text = re.sub(f"[{DRAWING_CHARACTERS}]", "", text)
        return text

    def to_html(self, text: str) -> str:
        state = self.State()
        buffer = ""

        for instruction in Ansi(text).instructions():
            if isinstance(instruction, str):

                classes: list[str] = []
                style_props: list[str] = []
                attributes: dict[str, str] = {}

                if state.blink:
                    # Blink should apply to all characters EXCEPT spaces (" ").
                    # So we need to split the string up and selectively wrap
                    # non-empty segments with blink tags.
                    inner = ""
                    for seg in self._split_spaces_pattern.findall(instruction):
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
