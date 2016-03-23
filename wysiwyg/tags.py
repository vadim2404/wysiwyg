# -*- coding: utf-8 -*-

import wysiwyg.exceptions


class Tag(object):
    name = None

    def __init__(self, attrs=None, children=None, *args, **kwargs):
        self.attrs = attrs or tuple()
        self.children = children or tuple()

    def validate(self):
        raise NotImplementedError('Method \'validate\' must be implemented.')

    def __iter__(self):
        return iter(self.children)


class TagRegistry(object):
    def __init__(self):
        self._tags = {}

    def register(self, tag):
        if not issubclass(tag, Tag):
            raise wysiwyg.exceptions.TagInstanceException(
                'Tag "%s" is not subclass of wysiwyg.tags.Tag.' % repr(tag)
            )

        if not isinstance(tag.name, str):
            raise wysiwyg.exceptions.TagNameIsInvalidException(
                'Tag name must be a string, but "%s" given.' % type(tag.name)
            )

        tag_name = tag.name.lower()
        if tag_name in self._tags:
            raise wysiwyg.exceptions.TagAlreadyRegisteredException(
                'Tag "%s" has been already registered.' % tag_name
            )

        self._tags[tag_name] = tag

    def __getitem__(self, item):
        return self._tags.get(item)

    def __iter__(self):
        return iter(self._tags)

    def __contains__(self, item):
        return item in self._tags


tag_registry = TagRegistry()


class PageTag(Tag):
    name = 'page'

    def validate(self):
        return not self.attrs


class Text(Tag):
    name = 'text_node'

    def validate(self):
        return not self.children


tag_registry.register(PageTag)
tag_registry.register(Text)
