from xml.etree.ElementTree import Element, SubElement

from core.constants.common import STR_EMPTY


def get_first_element_or_default(
    parent: Element, tag: str, text: str= STR_EMPTY, attrib: dict[str, str] | None = None
):
    if attrib is None:
        attrib = {}
    elements = [e for e in parent if e.tag == tag]
    if not any(elements):
        default_element = SubElement(parent, tag=tag, attrib=attrib, text=text)
        return default_element
    else:
        return elements[0]