import pytest
from transformations import build_drugs_dataframe

def test_build_drugs_dataframe():
    df_drugs = build_drugs_dataframe('../data/drugbank_partial.xml')
    assert len(df_drugs) > 0, 'Should have at least one row'
    assert 'drugbank_id' in df_drugs.columns, 'drugbank_id column should be present'