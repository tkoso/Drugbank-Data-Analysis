# we are using lxml for optimized efficiency when dealing with big xml data
from lxml import etree

NAMESPACE = '{http://www.drugbank.ca}'

def parse_drugbank_xml(xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()
    return root