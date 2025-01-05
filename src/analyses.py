import pandas as pd

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