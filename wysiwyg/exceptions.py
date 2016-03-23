# -*- coding: utf-8 -*-


class WysiwygException(Exception):
    pass


class TagInstanceException(WysiwygException):
    pass


class TagAlreadyRegisteredException(WysiwygException):
    pass


class TagNameIsInvalidException(WysiwygException):
    pass


class ParserInvalidArgumentException(WysiwygException):
    pass


class ParserParseException(WysiwygException):
    pass


class ParserUnregisteredTagException(WysiwygException):
    pass
