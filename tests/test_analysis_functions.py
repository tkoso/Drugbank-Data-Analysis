import pytest
import pandas as pd

from analyses import (
    count_unique_pathways,
    approved_and_non_withdrawn_drugs,
    count_pathways_per_drug
)

def test_count_unique_pathways():
    df_pathways = pd.DataFrame([
        {'pathway_name': 'Lepirudin Action Pathway', 'smpdb-id': 'SMP0000278'},
        {'pathway_name': 'Cetuximab Action Pathway', 'smpdb-id': 'SMP0000474'},
        {'pathway_name': 'Lepirudin Action Pathway', 'smpdb-id': 'SMP0000278'},
    ])
    result = count_unique_pathways(df_pathways)
    assert result == 2, f'Expected 2 unique pathways, got {result}.'

def test_approved_and_non_withdrawn_drugs():
    df_groups = pd.DataFrame([
        {'drugbank_id': 'DB00001', 'group': 'approved'},
        {'drugbank_id': 'DB00001', 'group': 'withdrawn'},
        {'drugbank_id': 'DB00002', 'group': 'approved'},
        {'drugbank_id': 'DB00004', 'group': 'approved'},
        {'drugbank_id': 'DB00004', 'group': 'investigational'},
    ])
    expected = 2
    result = approved_and_non_withdrawn_drugs(df_groups)
    assert result == expected, f'Expected {expected}, got {result}.'

def test_count_pathways_per_drug():
    df_pathways_to_drugs = pd.DataFrame([
        {
            'pathway_name': 'Lepirudin Action Pathway',
            'drugbank_id': 'DB00001',
            'smpdb-id': 'SMP0000278'
        },
        {
            'pathway_name': 'Lepirudin Action Pathway',
            'drugbank_id': 'DB01022',
            'smpdb-id': 'SMP0000278'
        },
        {
            'pathway_name': 'Cetuximab Action Pathway',
            'drugbank_id': 'DB00001',
            'smpdb-id': 'SMP0000474'
        },
    ])
    df_count = count_pathways_per_drug(df_pathways_to_drugs)
    assert set(df_count.columns) == {'drugbank_id', 'num_pathways'}, (
        f'Columns mismatch: {df_count.columns.tolist()}.'
    )
    res_dict = dict(zip(df_count['drugbank_id'], df_count['num_pathways']))
    assert res_dict.get('DB00001') == 2, f'Expected DB00001 => 2, got {res_dict.get("DB00001")}'
    assert res_dict.get('DB01022') == 1, f'Expected DB01022 => 1, got {res_dict.get("DB01022")}'
