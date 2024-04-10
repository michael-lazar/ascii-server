import logging
from dataclasses import dataclass

from django.utils.html import escape
from django.utils.safestring import mark_safe
from stransi import Ansi, SetAttribute, SetColor
from stransi.attribute import Attribute
from stransi.color import ColorRole

_logger = logging.getLogger(__name__)


@dataclass
class State:
    fg: int = 7
    bg: int = 0
    bold: bool = False


class ANSIParser:

    def to_html(self, data: bytes) -> str:
        text = data.decode("gb18030", errors="replace")

        state = State()
        buffer: list[str] = []

        for instruction in Ansi(text).instructions():
            if isinstance(instruction, str):
                style_props: list[str] = []

                if state.bold:
                    style_props.append(f"color: var(--c{state.fg + 8})")
                else:
                    style_props.append(f"color: var(--c{state.fg})")

                style_props.append(f"background-color: var(--c{state.bg})")

                style = "; ".join(style_props)
                element = f"<span style='{style}'>{escape(instruction)}</span>"
                buffer.append(element)

            elif isinstance(instruction, SetColor):
                if instruction.color.code < 8:
                    match instruction.role:
                        case ColorRole.FOREGROUND:
                            state.fg = instruction.color.code
                        case ColorRole.BACKGROUND:
                            state.bg = instruction.color.code
                        case _:
                            raise ValueError
                else:
                    _logger.warning(f"Unhandled ANSI: {instruction}")

            elif isinstance(instruction, SetAttribute):

                match instruction.attribute:
                    case Attribute.NORMAL:
                        state = State()
                    case Attribute.BOLD:
                        state.bold = True
                    case _:
                        _logger.warning(f"Unhandled ANSI: {instruction}")

            else:
                _logger.warning(f"Unhandled ANSI: {instruction}")

        ansi = "".join(buffer)
        return mark_safe(ansi)
