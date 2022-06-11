import re


JSON_REGEX = re.compile('^.+\.json$')
XML_REGEX = re.compile('^.+\.xml$')


def is_json(file):
    return bool(JSON_REGEX.match(file))


def is_xml(file):
    return bool(XML_REGEX.match(file))