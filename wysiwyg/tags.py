# -*- coding: utf-8 -*-

from . import exceptions

__all__ = (
    'Tag',
    'ChildrenValidatorMixin',
    'PageTag',
    'Text',
    'TagRegistry',
    'tag_registry',
)


class Tag(object):
    name = None

    def __init__(self, attrs=None, children=None, *args, **kwargs):
        self.attrs = attrs or tuple()
        self.children = children or tuple()

    def is_valid(self):
        raise NotImplementedError('Method \'validate\' must be implemented.')

    def __iter__(self):
        return iter(self.children)


class ChildrenValidatorMixin(object):
    def is_valid(self):
        return all(node.is_valid() for node in self.children)


class PageTag(ChildrenValidatorMixin, Tag):
    name = 'page'

    def is_valid(self):
        return not self.attrs and super(PageTag, self).is_valid()


class Text(Tag):
    name = 'text_node'

    def is_valid(self):
        return 'value' in self.attrs and len(self.attrs) == 1 and not self.children


class TagRegistry(object):
    def __init__(self):
        self._tags = {}
        self.register(PageTag)
        self.register(Text)

    def register(self, tag):
        if not issubclass(tag, Tag):
            raise exceptions.TagInstanceException(
                'Tag "%s" is not subclass of wysiwyg.tags.Tag.' % repr(tag)
            )

        if not isinstance(tag.name, str):
            raise exceptions.TagNameIsInvalidException(
                'Tag name must be a string, but "%s" given.' % type(tag.name)
            )

        tag_name = tag.name.lower()
        if tag_name in self._tags:
            raise exceptions.TagAlreadyRegisteredException(
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
