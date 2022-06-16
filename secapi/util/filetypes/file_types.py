import re


JSON_FILE = '.json'
XML_FILE = '.xml'

JSON_FILE_REGEX = re.compile('^.*\.json$')
XML_FILE_REGEX = re.compile('^.*\.xml$')


def is_json_file(file):
    return bool(JSON_FILE_REGEX.match(file))


def is_xml_file(file):
    return bool(XML_FILE_REGEX.match(file))