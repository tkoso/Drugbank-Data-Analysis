import pytest
from transformations import build_drugs_dataframe
from parsing import parse_drugbank_xml

def test_build_drugs_dataframe():
    root = parse_drugbank_xml('../data/drugbank_partial.xml')
    df_drugs = build_drugs_dataframe(root)
    assert len(df_drugs) > 0, 'Should have at least one row'
    assert 'drugbank_id' in df_drugs.columns, 'drugbank_id column should be present'