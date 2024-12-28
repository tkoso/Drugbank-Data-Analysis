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