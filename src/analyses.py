import pandas as pd

def count_unique_pathways(df_pathways):
    return df_pathways['pathway_name'].nunique()