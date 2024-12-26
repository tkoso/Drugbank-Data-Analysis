import xml.etree.ElementTree as ET
import pandas as pd

NAMESPACE = '{http://www.drugbank.ca}'

def parse_drugbank_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return root