import pytest
from parsing import parse_drugbank_xml

NAMESPACE = '{http://www.drugbank.ca}'

def test_count_100_drugs_in_xml():
    root = parse_drugbank_xml('../data/drugbank_partial.xml')
    
    drugs = root.findall(f"{NAMESPACE}drug")
    assert len(drugs) == 100, f'Expected 100 <drug> elements, found {len(drugs)}.'


def test_no_empty_drug_names_in_xml():
    root = parse_drugbank_xml('../data/drugbank_partial.xml')

    drugs = root.findall(f"{NAMESPACE}drug")
    assert len(drugs) > 0, 'No <drug> elements found at all!'

    for d in drugs:
        drug_name = d.findtext(f'{NAMESPACE}name')
        
        # Ensure drug_name is not None or an empty string
        assert drug_name is not None, 'A <drug> element is missing a <name> tag!'
        assert drug_name.strip() != '', '<name> tag is present but it\'s empty!'
