import pandas as pd
import numpy as np
import pickle

from openai import OpenAI
import numpy as np
import pandas as pd
from pathlib import Path

MODEL = "text-embedding-embeddinggemma-300m-qat"
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)
def get_embedding(text:str, model="model-identifier"):
   text = text.replace("\n", " ")
   
   embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
   return np.array(embedding)

symptoms_embeddings_path = Path('../data/symptomes_embedding.pkl')

if not symptoms_embeddings_path.is_absolute():
            # resolve relative to the repository/code file location (works on Windows)
            symptoms_embeddings_path = (Path(__file__).resolve().parent / symptoms_embeddings_path).resolve()

with open(symptoms_embeddings_path, 'rb') as fp:
        symptoms_embeds = pickle.load(fp)


def distance_rep_patient(rep_patient:str) : 
    rep_embedding  = get_embedding(rep_patient)

    criteria_embedding = np.stack(symptoms_embeds['embedding'])

    distance = rep_embedding@criteria_embedding.T

    patient_frame = symptoms_embeds[['symptome']].copy()

    # display(patient_frame)

    patient_frame['score'] = distance

    return patient_frame 
