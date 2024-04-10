from ansi2html import Ansi2HTMLConverter


class ANSIParser:

    def __init__(self):
        self.converter = Ansi2HTMLConverter()

    def to_html(self, data: bytes) -> str:
        text = data.decode("gb18030", errors="replace")
        html = self.converter.convert(text, full=True)
        return html
