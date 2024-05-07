import os
import re
import time

from lxml import etree


def unescape_xml_text(text: str) -> str:
    """
    Reverse the sanitization that was done by fbbs in order to embed
    the ANSI screen into an XML document.

    Reference:
        https://github.com/fbbs/fbbs/blob/master/fcgi/libweb.c#L78
    """
    text = re.sub(">1b", "\x1b", text)
    text = re.sub("&lt;", "<", text)
    text = re.sub("&gt;", ">", text)
    text = re.sub("&amp;", "&", text)
    text = re.sub("\n", "\r\n", text)
    return text


def unescape_xml_bytes(data: bytes) -> bytes:
    """
    Reverse the sanitization that was done by fbbs in order to embed
    the ANSI screen into an XML document.

    Reference:
        https://github.com/fbbs/fbbs/blob/master/fcgi/libweb.c#L78
    """
    data = re.sub(b">1b", b"\x1b", data)
    data = re.sub(b"&lt;", b"<", data)
    data = re.sub(b"&gt;", b">", data)
    data = re.sub(b"&amp;", b"&", data)
    data = re.sub(b"\n", b"\r\n", data)
    return data


def parse_xml(data: bytes, recover: bool = False) -> etree.ElementTree:
    parser = etree.XMLParser(recover=recover)
    root = etree.fromstring(data, parser=parser)
    return root


_xml_document_pattern = re.compile(rb"<po>(.*?)</po>", re.DOTALL)


def parse_xml_re(data: bytes) -> bytes:
    """
    Sometimes the encoded ANSI has invalid byte-sequences, so we need
    to be fault-tolerant. Parsing using a regex and then decoding the
    data directly in python gives us more control over how errors are
    handled versus using lxml.

    For example, see this URL which breaks the javascript on the web portal:
        https://bbs.fudan.edu.cn/bbs/anc?path=/groups/rec.faq/ANSI/recommend/D6F3FF4AE/G.1071333485.430613
    """
    if m := _xml_document_pattern.search(data):
        return m.group(1)

    return b""


def get_ansi_length(text: str) -> int:
    """
    Returns the length of a string, as it would be rendered in a terminal window.
    """
    return len(text.encode("gb18030"))


def screenshot_page(url: str, output_dir: str, font_size: int = 24):
    """
    Open the given fudan URL in selenium and automate capturing screenshots.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    os.makedirs(output_dir, exist_ok=True)

    width = font_size * 41
    height = font_size * 22

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    time.sleep(0.1)  # Allow page to load

    # Adjust window size to ensure the viewport size is correct
    inner_height = driver.execute_script("return window.innerHeight")
    outer_height = driver.execute_script("return window.outerHeight")

    chrome_height = outer_height - inner_height

    # Set the window size to account for the chrome
    driver.set_window_size(width, height + chrome_height)

    scroll_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("return document.body.style.overflow = 'hidden';")

    current_scroll_position = 0
    screenshot_count = 0

    while current_scroll_position < scroll_height:
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position})")
        time.sleep(0.1)  # Allow scroll to finish

        filename = os.path.join(output_dir, f"screenshot_{screenshot_count:>04}.png")
        driver.save_screenshot(filename)
        yield filename

        current_scroll_position += height
        screenshot_count += 1

    driver.quit()
