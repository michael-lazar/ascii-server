import asyncio

import requests
from django.core.management.base import BaseCommand, CommandParser
from telnetlib3 import create_server, telopt

from ascii.fudan.utils import parse_xml_re, unescape_xml_bytes


class TelnetServer:
    """
    A simple async telnet server.
    """

    def __init__(self, host: str, port: int):
        self.data = b""
        self.server = create_server(
            host=host,
            port=port,
            shell=self.shell,
            encoding=False,
        )

    def load_data(self, url: str) -> None:
        resp = requests.get(url)

        data = parse_xml_re(resp.content)
        data = unescape_xml_bytes(data)
        self.data = data

    def run_forever(self):
        loop = asyncio.get_event_loop()
        coro = loop.run_until_complete(self.server)
        loop.run_until_complete(coro.wait_closed())

    async def shell(self, reader, writer) -> None:
        try:
            await self.handle(reader, writer)
        except ConnectionError:
            pass

    async def handle(self, reader, writer) -> None:
        writer.iac(telopt.DO, telopt.NAWS)
        writer.iac(telopt.DO, telopt.SGA)
        writer.iac(telopt.WILL, telopt.SGA)
        writer.iac(telopt.WILL, telopt.ECHO)
        writer.iac(telopt.WONT, telopt.LINEMODE)

        await asyncio.sleep(0.5)

        writer.write(b"\x1b[H")  # Reset cursor

        for line in self.data.splitlines(keepends=True):
            writer.write(line)
            await writer.drain()

            while True:
                try:
                    char = await asyncio.wait_for(reader.read(1), timeout=0.1)
                    if char == b" ":
                        # Print a new line when the space bar is pressed
                        break
                except TimeoutError:
                    pass

        writer.close()


class Command(BaseCommand):
    help = "Mirror the given URL over telnet, for testing with BBS clients"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("url", help="Source URL")
        parser.add_argument("--host", default="0.0.0.0", help="Telnet server host")
        parser.add_argument("--port", default=23, type=int, help="Telnet server port")

    def handle(self, *args, **options):
        server = TelnetServer(options["host"], options["port"])
        server.load_data(options["url"])
        server.run_forever()
