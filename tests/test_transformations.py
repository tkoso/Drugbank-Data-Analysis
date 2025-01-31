import pytest
from transformations import (
    build_drugs_dataframe,
    build_synonyms_dataframe
)
from parsing import parse_drugbank_xml

def test_build_drugs_dataframe():
    root = parse_drugbank_xml('../data/drugbank_partial.xml')
    df_drugs = build_drugs_dataframe(root)
    assert len(df_drugs) > 0, 'Should have at least one row'
    assert 'drugbank_id' in df_drugs.columns, 'drugbank_id column should be present'

def test_build_synonyms_dataframe_non_empty():
    root = parse_drugbank_xml('../data/drugbank_partial.xml')
    df_synonyms = build_synonyms_dataframe(root)
    assert len(df_synonyms) > 0, 'Should have at least one row'
    assert 'drugbank_id' in df_synonyms.columns, 'drugbank_id column should be present'
    assert 'synonym' in df_synonyms.columns, 'synonym column should be present'

@pytest.mark.parametrize('drug_id, synonym', [
    ('DB00001', 'Desulfatohirudin'),
    ('DB00002', 'Cetuximab'),
])
def test_synonyms_include(drug_id, synonym):
    root = parse_drugbank_xml('../data/drugbank_partial.xml')
    df_synonyms = build_synonyms_dataframe(root)
    synonyms = df_synonyms[df_synonyms['drugbank_id'] == drug_id]['synonym'].tolist()
    assert synonym in synonyms

# do mocking test
from unittest.mock import Mock
from transformations import build_pathways_to_drugs_dataframe

import pytest
import pandas as pd
from unittest.mock import Mock
from transformations import build_pathways_to_drugs_dataframe, NAMESPACE

def test_build_pathways_to_drugs_dataframe():
    root_mock = Mock() # This simulates the "root"
    drug_mock = Mock() # This simulates <drug>
    pathway_mock = Mock() # This simulates <pathway>
    pathway_drug_mock = Mock() # This simulates <drugs><drug>

    root_mock.findall.return_value = [drug_mock]

    drug_mock.findall.return_value = [pathway_mock]

    def pathway_findtext_side_effect(arg):
        if arg.endswith('name'):
            return 'pathway_name'
        elif arg.endswith('smpdb-id'):
            return 'SMP123'
        return None

    pathway_mock.findtext.side_effect = pathway_findtext_side_effect
    pathway_mock.findall.return_value = [pathway_drug_mock]

    pathway_drug_mock.findtext.return_value = 'DB00001'

    df_pathways = build_pathways_to_drugs_dataframe(root_mock)

    assert len(df_pathways) == 1, 'Should return exactly one record'
    assert list(df_pathways.columns) == ['pathway_name', 'drugbank_id', 'smpdb-id'], \
        'Expected columns pathway_name, drugbank_id, smpdb-id'

    row = df_pathways.iloc[0]
    assert row['pathway_name'] == 'pathway_name'
    assert row['drugbank_id'] == 'DB00001'
    assert row['smpdb-id'] == 'SMP123'
