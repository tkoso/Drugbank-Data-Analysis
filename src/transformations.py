import pandas as pd
from .parsing import parse_drugbank_xml, NAMESPACE

def build_drugs_dataframe(xml_path):
    root = parse_drugbank_xml(xml_path)
    records = []

    for drug in root.findall(f'{NAMESPACE}drug'):
        drug_id = drug.findtext(f'{NAMESPACE}drugbank-id[@primary="true"]')
        name = drug.findtext(f'{NAMESPACE}name')
        drug_type = drug.get('type')
        description = drug.findtext(f'{NAMESPACE}description')
        dosage_form = drug.findtext(f'{NAMESPACE}dosage-form')
        indication = drug.findtext(f'{NAMESPACE}indication')
        mechanism_of_action = drug.findtext(f'{NAMESPACE}mechanism-of-action')
        food_nodes = drug.findall(f'{NAMESPACE}food-interactions/{NAMESPACE}food-interaction')
        food_interactions = [fn.text for fn in food_nodes]

        records.append({
            'drugbank_id': drug_id,
            'name': name,
            'type': drug_type,
            'description': description,
            'dosage_form': dosage_form,
            'indication': indication,
            'mechanism_of_action': mechanism_of_action,
            'food_interactions': '; '.join(food_interactions)
        })

    return pd.DataFrame(records) 