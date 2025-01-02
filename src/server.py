from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from transformations import build_pathways_dataframe
# TODO: import analysing function

app = FastAPI()

class DrugID(BaseModel):
    drugbank_id: str

df_pathways_global = None


@app.on_event('startup')
def load_data():
    global df_pathways_global
    df_pathways_global = build_pathways_dataframe('../data/drugbank_partial.xml')

@app.post('/pathways')
def get_pathways(drug_id: DrugID):
    global df_pathways_global

    # TODO: add the analysis part
    ans = drug_id.drugbank_id

    return ans


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)