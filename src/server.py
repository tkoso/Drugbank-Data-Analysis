from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from transformations import build_pathways_to_drugs_dataframe
from analyses import count_pathways_per_drug
from parsing import parse_drugbank_xml


app = FastAPI()

# The client must send a JSON with a field "drugbank_id" as a string.
class DrugID(BaseModel):
    drugbank_id: str

df_pathways_count_per_drug_global = None


# This function is executed when the server starts.
@app.on_event('startup')
def load_data():
    root = parse_drugbank_xml('../data/drugbank_partial.xml')
    global df_pathways_count_per_drug_global
    df_pathways_to_drugs = build_pathways_to_drugs_dataframe(root)
    df_pathways_count_per_drug_global = count_pathways_per_drug(df_pathways_to_drugs)


# Define a POST endpoint at "/pathways" to receive a drug id and return the associated pathway count.
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