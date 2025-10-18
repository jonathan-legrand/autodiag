import pandas as pd
import numpy as np
import pickle

from openai import OpenAI
import numpy as np
import pandas as pd

MODEL = "text-embedding-embeddinggemma-300m-qat"
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)
def get_embedding(text, model="model-identifier"):
   text = text.replace("\n", " ")
   
   embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
   return np.array(embedding)

with open('../data/symptomes_embedding.pkl', 'rb') as fp:
        symptoms_embeds = pickle.load(fp)


def distance_rep_patient(rep_patient:str) : 
    
    rep_embedding  = get_embedding(rep_patient)

    criteria_embedding = np.stack(symptoms_embeds['embedding'])

    distance = rep_embedding@criteria_embedding.T

    patient_frame = symptoms_embeds[['symptome']]

    # display(patient_frame)

    patient_frame['score'] = distance

    return patient_frame 




example_patient = distance_rep_patient('Hello I am sad', symptoms_embeds)

example_patient.to_csv('../data/example_patient.csv')