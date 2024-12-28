import pandas as pd
from parsing import parse_drugbank_xml, NAMESPACE

def build_drugs_dataframe(xml_path):
    root = parse_drugbank_xml(xml_path)
    records = []

    for drug in root.findall(f'{NAMESPACE}drug'):
        drug_id = drug.findtext(f'{NAMESPACE}drugbank-id[@primary="true"]')
        name = drug.findtext(f'{NAMESPACE}name')
        drug_type = drug.get('type')
        description = drug.findtext(f'{NAMESPACE}description')
        # TODO: something doesn't work here with the dosage_form, it's inside the <products> tag...
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

def build_synonyms_dataframe(xml_path):
    root = parse_drugbank_xml(xml_path)
    records = []

    for drug in root.findall(f'{NAMESPACE}drug'):
        drug_id = drug.findtext(f'{NAMESPACE}drugbank-id[@primary="true"]')
        synonyms = drug.findall(f'{NAMESPACE}synonyms/{NAMESPACE}synonym')
        for synonym in synonyms:
            records.append({
                'drugbank_id': drug_id,
                'synonym': synonym.text
            })

    return pd.DataFrame(records) # next step is to draw a synonym graph out of this df


def build_products_dataframe(xml_path):
    root = parse_drugbank_xml(xml_path)
    records = []

    for drug in root.findall(f'{NAMESPACE}drug'):
        drug_id = drug.findtext(f'{NAMESPACE}drugbank-id[@primary="true"]')
        for product in drug.findall(f'{NAMESPACE}products/{NAMESPACE}product'):
            name = product.findtext(f'{NAMESPACE}name')
            labeller = product.findtext(f'{NAMESPACE}labeller')
            ndc_product_code = product.findtext(f'{NAMESPACE}ndc-product-code')
            dosage_form = product.findtext(f'{NAMESPACE}dosage-form')
            route = product.findtext(f'{NAMESPACE}route')
            strength = product.findtext(f'{NAMESPACE}strength')
            country = product.findtext(f'{NAMESPACE}country')
            source = product.findtext(f'{NAMESPACE}source')

            records.append({
                'drugbank_id': drug_id,
                'product_name': name,
                'labeller': labeller,
                'ndc_product_code': ndc_product_code,
                'dosage_form': dosage_form,
                'route': route,
                'strength': strength,
                'country': country,
                'source': source
            })

    return pd.DataFrame(records)

def build_pathways_dataframe(xml_path):
    root = parse_drugbank_xml(xml_path)
    records = []

    for drug in root.findall(f'{NAMESPACE}drug'):
        drug_id = drug.findtext(f'{NAMESPACE}drugbank-id[@primary="true"]')
        pathways = drug.findall(f'{NAMESPACE}pathways/{NAMESPACE}pathway')
        for pathway in pathways:
            pathway_name = pathway.findtext(f'{NAMESPACE}name')
            pathway_smpdb = pathway.findtext(f'{NAMESPACE}smpdb-id')
            records.append({
                'drugbank_id': drug_id,
                'pathway_name': pathway_name,
                'smpdb-id': pathway_smpdb
            })

    return pd.DataFrame(records)


