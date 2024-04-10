import re

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
    data = _xml_document_pattern.search(data).group(1)
    return data
