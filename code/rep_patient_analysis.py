import pandas as pd
import numpy as np
import pickle

from openai import OpenAI
import numpy as np
import pandas as pd
from pathlib import Path
import os
from text_preprocessing import preprocess_sentence
from dotenv import load_dotenv
from llm_query import call_api
load_dotenv()
base_url = os.getenv("LMSTUDIO_BASE_URL")
MODEL = os.getenv("LMSTUDIO_MODEL")
client = OpenAI(
    base_url=base_url,
    api_key="lm-studio"
)
def get_embedding(text:str, model=MODEL):
   text = text.replace("\n", " ")
   
   embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
   return np.array(embedding)

symptoms_embeddings_path = Path('../data/symptomes_embedding.pkl')

if not symptoms_embeddings_path.is_absolute():
            # resolve relative to the repository/code file location (works on Windows)
            symptoms_embeddings_path = (Path(__file__).resolve().parent / symptoms_embeddings_path).resolve()

with open(symptoms_embeddings_path, 'rb') as fp:
        symptoms_embeds = pickle.load(fp)

def reformulate_patient_response(rep_patient:str):
    prompt = f"""
    Extract and list the symptoms mentioned in the following patient response. 
    Describe the symptoms in a few sentences, in terms related to mental health.
    Reformulated multiple times the description of each symptoms
    if no symptoms are mentioned, respond with 'nothing to declare'.
    Return the symptoms description as comma separated list of long descriptions.
    do not mention anything other than these descriptions.
    Include only positive findings; omit any negated or absent ones.
    Patient Response: "{rep_patient}"
    """
    response = call_api([{"role": "user", "content": prompt}], role="patient")

    contains_symptoms = True
    if "no symptoms" in response.lower():
        contains_symptoms = False
    response = response.split(",")
    return response, contains_symptoms

def distance_rep_patient(rep_patient:str, preprocess=False):
    if preprocess:
        rep_patient = preprocess_sentence(rep_patient) 
    rep_embedding  = get_embedding(rep_patient)

    criteria_embedding = np.stack(symptoms_embeds['embedding'])

    distance = rep_embedding @ criteria_embedding.T

    # keep on
    thr = np.min((np.percentile(distance, 99.9), 0.99))
    distance = np.where(distance >= thr, 1, 0)
    # extract only max value
    # distance = np.where(distance == np.max(distance), 1, 0)

    patient_frame = symptoms_embeds[['symptome']].copy()

    # display(patient_frame)

    patient_frame['score'] = distance

    return patient_frame
