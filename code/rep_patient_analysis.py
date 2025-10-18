from query_embedding import get_embedding
import pandas as pd
import numpy as np
import pickle

with open('../data/symptomes_embedding.pkl', 'rb') as fp:
        symptoms_embeds = pickle.load(fp)


def distance_rep_patient(rep_patient:str, symptomes_embedding) : 
    
    rep_embedding  = get_embedding(rep_patient)

    criteria_embedding = np.stack(symptoms_embeds['embedding'])

    distance = rep_embedding@criteria_embedding.T

    patient_frame = symptoms_embeds[['symptome']]

    # display(patient_frame)

    patient_frame['score'] = distance

    return patient_frame 




example_patient = distance_rep_patient('Hello I am sad', symptoms_embeds)

example_patient.to_csv('../data/example_patient.csv')