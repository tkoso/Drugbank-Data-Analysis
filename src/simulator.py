from lxml import etree as ET  # or from xml.etree import ElementTree as ET if you prefer
from parsing import parse_drugbank_xml, NAMESPACE
from copy import deepcopy
import random


def _collect_drug_columns(root):
    """
    Iterate over all drug elements and collect each child's XML string,
    except for the drugbank-id element which is handled separately.
    Returns a dictionary mapping tag names to a list of XML strings.
    """
    drugs = root.findall(f'{NAMESPACE}drug')
    child_map = {}

    for drug in drugs:
        for child in drug:
            # Skip the drugbank-id element to avoid sampling it.
            if child.tag == f'{NAMESPACE}drugbank-id':
                continue
            tag_name = child.tag # e.g., "{NAMESPACE}products"
            xml_string = ET.tostring(child, encoding='unicode')
            if tag_name not in child_map:
                child_map[tag_name] = []
            child_map[tag_name].append(xml_string)

    return child_map


def generate_drugs(xml_in, xml_out, total_drugs=20000):
    """
    Generate new drug entries by copying a template drug, manually updating the drugbank-id,
    and appending randomly chosen child elements (except for drugbank-id).
    The resulting XML is written to the specified output file.
    """
    root = parse_drugbank_xml(xml_in)
    tree = ET.ElementTree(root)

    original_drugs = root.findall(f'{NAMESPACE}drug')

    # collect the XML string versions of each child element, excluding drugbank-id
    child_map = _collect_drug_columns(root)
    
    # use the first drug element as a template
    template_drug = original_drugs[0]

    start_new_id = 109  # starting point manually checked
    end_new_id = start_new_id + (total_drugs - 100)

    for new_id in range(start_new_id, end_new_id + 1):
        new_drug = deepcopy(template_drug)

        # update the drugbank-id element with the new id.
        new_drugbank_id = new_drug.find(f'{NAMESPACE}drugbank-id')
        if new_drugbank_id is not None:
            new_drugbank_id.text = f"DB{new_id:05d}"

        # remove all children except for the drugbank-id element.
        for child in list(new_drug):
            if child.tag != f'{NAMESPACE}drugbank-id':
                new_drug.remove(child)

        # for each type of child element, choose one at random from our collected pool.
        for tag_name, xml_strings in child_map.items():
            chosen_str = random.choice(xml_strings)
            new_child = ET.fromstring(chosen_str)
            new_drug.append(new_child)

        # append the new drug element to the root.
        root.append(new_drug)

    # here we write the updated XML tree to the output file.
    tree.write(xml_out, encoding='utf-8', xml_declaration=True, pretty_print=True)
