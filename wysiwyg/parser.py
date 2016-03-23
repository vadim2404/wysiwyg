# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as ElementTree

try:
    from html import escape
except ImportError:
    from cgi import escape

import wysiwyg.exceptions
from wysiwyg.tags import tag_registry


__all__ = (
    'parse',
)


TEXT_NODE_REGEX = re.compile(r'>([^<]+)<', re.MULTILINE | re.IGNORECASE | re.UNICODE)


def parse(text, *args, **kwargs):
    if not isinstance(text, str):
        raise wysiwyg.exceptions.ParserInvalidArgumentException(
            'Text must be a string, but "%s" given.' % type(text)
        )

    formatted_text = TEXT_NODE_REGEX.sub(
        lambda match: '><text_node value="%s"></text_node><' % escape(match.group(1)), text
    )
    wrapped_text = '<?xml version="1.0"?><page>%s</page>' % formatted_text

    try:
        tree = ElementTree.fromstring(wrapped_text)
    except ElementTree.ParseError:
        raise wysiwyg.exceptions.ParserParseException(
            'Text must be a valid XML-document.'
        )

    def create_tree(node):
        tag_name = node.tag.lower()

        if not tag_name in tag_registry:
            raise wysiwyg.exceptions.ParserUnregisteredTagException(
                'Tag "%s" is not registered.' % tag_name
            )

        children = []

        for child in node:
            children.append(create_tree(child))

        kwargs.update({
            'attrs': node.attrib,
            'children': children,
        })
        return tag_registry[tag_name](*args, **kwargs)

    return create_tree(tree)