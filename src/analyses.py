import pandas as pd
import requests
import time

def count_unique_pathways(df_pathways):
    return df_pathways['pathway_name'].nunique()


def approved_and_non_withdrawn_drugs(df_groups):
    grouped = df_groups.groupby('drugbank_id')['group'].apply(set)

    count = sum(('approved' in group_set) and not ('withdrawn' in group_set) for group_set in grouped)

    return count
    
def count_pathways_per_drug(df_pathways_to_drugs):
    grouped = (
        df_pathways_to_drugs
        .groupby('drugbank_id')['pathway_name']
        .nunique()
        .reset_index()
        .rename(columns={'pathway_name': 'num_pathways'})
    )
    return grouped


def _fetch_uniprot_data(gene_name):
    base_url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": f"gene:{gene_name}",
        "format": "json",
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

def _extract_disease_ids(json_data):
    diseases = set()
    
    # Iterate through all entries in results
    for entry in json_data.get("results", []):
        # Check each comment in the entry
        for comment in entry.get("comments", []):
            if comment.get("commentType") == "DISEASE":
                disease_info = comment.get("disease", {})
                name = disease_info.get("diseaseId")
                if name:
                    diseases.add(f"{name}")
    
    return list(diseases)

def _fetch_diseases_from_uniprot(gene_name):
    uniprot_json = _fetch_uniprot_data(gene_name)
    return _extract_disease_ids(uniprot_json)


def get_diseases_related_to_drug(df_targets, drug_id):
    """
    1) Filters df_targets by drug_id.
    2) For each unique gene, calls _fetch_diseases_from_uniprot(gene).
    3) Aggregates results into one list of records.
    4) Returns a DataFrame of drugbank_id, gene_name, and disease.
    """

    # Filter the DataFrame to rows matching the given drug_id
    df_filtered = df_targets[df_targets['drugbank_id'] == drug_id]

    # Get unique gene names for that drug
    unique_genes = df_filtered['gene_name'].dropna().unique()

    records = []

    for gene in unique_genes:
        if not gene:
            continue

        diseases = _fetch_diseases_from_uniprot(gene)

        if diseases:
            # For each disease, create a record
            for disease in diseases:
                records.append({
                    "drugbank_id": drug_id,
                    "gene_name": gene,
                    "disease": disease
                })
        else:
            # If no diseases were found, store "No info"
            records.append({
                "drugbank_id": drug_id,
                "gene_name": gene,
                "disease": "No info"
            })

        time.sleep(0.5)  # Avoid overloading the API

    # Convert all collected records to a DataFrame
    df_result = pd.DataFrame(records)
    return df_result