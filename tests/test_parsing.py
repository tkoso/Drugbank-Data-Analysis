import pytest
from parsing import parse_drugbank_xml

def test_parse_drugbank_xml():
    root = parse_drugbank_xml('../data/drugbank_partial.xml')
    assert root is not None, 'XML root should not be None'