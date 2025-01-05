from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from transformations import build_pathways_to_drugs_dataframe
from analyses import count_pathways_per_drug

XML_PATH = '../data/drugbank_partial.xml'
app = FastAPI()

class DrugID(BaseModel):
    drugbank_id: str

df_pathways_count_per_drug_global = None


@app.on_event('startup')
def load_data():
    global df_pathways_count_per_drug_global
    df_pathways_to_drugs = build_pathways_to_drugs_dataframe(XML_PATH)
    df_pathways_count_per_drug_global = count_pathways_per_drug(df_pathways_to_drugs)

@app.post('/pathways')
def get_pathways(drug_id: DrugID):
    global df_pathways_count_per_drug_global

    ans = None
    filtered_row = df_pathways_count_per_drug_global.loc[df_pathways_count_per_drug_global['drugbank_id'] == drug_id.drugbank_id, 'num_pathways']
    if not filtered_row.empty:
        ans = str(filtered_row.iloc[0])
    else:
        ans = 'No pathways found.'

    return ans


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)