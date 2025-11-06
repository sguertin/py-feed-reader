from xml.etree.ElementTree import Element, SubElement

from core.constants.common import EMPTY_STRING


def get_first_element_or_default(
    parent: Element,
    tag: str,
    text: str = EMPTY_STRING,
    attrib: dict[str, str] | None = None,
):
    if attrib is None:
        attrib = {}
    elements = [e for e in parent if e.tag == tag]
    if not any(elements):
        default_element = Element(tag, attrib=attrib, text=text)
        parent.append(default_element)
        return default_element
    else:
        return elements[0]
