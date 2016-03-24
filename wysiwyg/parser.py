# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as ElementTree

try:
    from html import escape
except ImportError:
    from cgi import escape

from . import exceptions
from .tags import tag_registry, TagRegistry

__all__ = (
    'parse',
)


TEXT_NODE_REGEX = re.compile(r'>([^<]+)<', re.MULTILINE | re.IGNORECASE | re.UNICODE)


def parse(text, registry=None, *args, **kwargs):
    if not isinstance(text, str):
        raise exceptions.ParserInvalidArgumentException(
            'Text must be a string, but "%s" given.' % type(text)
        )

    registry = registry or tag_registry
    if not isinstance(registry, TagRegistry):
         raise exceptions.ParserInvalidArgumentException(
             'Registry must be an instance of wysiwyg.tags.TagRegistry, bug "%s" given.' % type(registry)
         )

    formatted_text = TEXT_NODE_REGEX.sub(
        lambda match: '><text_node value="%s"></text_node><' % escape(match.group(1)), text
    )
    wrapped_text = '<?xml version="1.0"?><page>%s</page>' % formatted_text

    try:
        tree = ElementTree.fromstring(wrapped_text)
    except ElementTree.ParseError:
        raise exceptions.ParserParseException(
            'Text must be a valid XML-document.'
        )

    def create_tree(node):
        tag_name = node.tag.lower()

        if not tag_name in tag_registry:
            raise exceptions.ParserUnregisteredTagException(
                'Tag "%s" is not registered.' % tag_name
            )

        kwargs.update({
            'attrs': node.attrib,
            'children': [create_tree(child) for child in node],
        })
        return tag_registry[tag_name](*args, **kwargs)

    return create_tree(tree)