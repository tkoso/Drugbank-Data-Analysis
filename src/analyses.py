import pandas as pd

def count_unique_pathways(df_pathways):
    return df_pathways['pathway_name'].nunique()

# def map_pathways_to_drugs(df_pathways):
#     grouped = (
#         df_pathways
#         .groupby('drugbank_id')['pathway_name']
#         .apply(list)
#         .reset_index()
#     )
#     return grouped

def approved_and_non_withdrawn_drugs(df_groups):
    grouped = df_groups.groupby('drugbank_id')['group'].apply(set)

    count = sum(('approved' in group_set) and not ('withdrawn' in group_set) for group_set in grouped)

    return count
    