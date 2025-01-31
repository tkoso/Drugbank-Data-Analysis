import xml.etree.ElementTree as ET
from parsing import parse_drugbank_xml, NAMESPACE
from copy import deepcopy
import random

ET.register_namespace('', NAMESPACE.strip('{}'))


def _collect_drug_columns(xml_path: str):
    root = parse_drugbank_xml(xml_path)
    
    drugs = root.findall(f'{NAMESPACE}drug')

    child_map = {}

    for drug in drugs:
        for child in drug:
            tag_name = child.tag # np. {NAMESPACE}products
            
            xml_string = ET.tostring(child, encoding='unicode')

            if tag_name not in child_map:
                child_map[tag_name] = []

            child_map[tag_name].append(xml_string)

    return child_map


def generate_drugs(xml_in: str, xml_out: str, total_drugs=20000):
    tree = ET.parse(xml_in)
    root = tree.getroot()

    original_drugs = root.findall(f'{NAMESPACE}drug')

    child_map = _collect_drug_columns(xml_in)
    
    template_drug = original_drugs[0] # TODO: think if that's what we want to do

    start_new_id = 109 # checked manually the value
    end_new_id = start_new_id + (total_drugs - 100)

    for new_id in range(start_new_id, end_new_id + 1):
        new_drug = deepcopy(template_drug)

        new_drugbank_id = new_drug.find(f'{NAMESPACE}drugbank-id')
        if new_drugbank_id is not None:
            new_drugbank_id.text = str(new_id)

        for child in list(new_drug):
            if child.tag != f'{NAMESPACE}drugbank-id':
                new_drug.remove(child)

        for tag_name, xml_strings in child_map.items():
            chosen_str = random.choice(xml_strings)

            new_child = ET.fromstring(chosen_str)
            new_drug.append(new_child)

        root.append(new_drug)

    tree.write(xml_out, encoding='utf-8', xml_declaration=True)


