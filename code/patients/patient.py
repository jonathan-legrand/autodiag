import pandas as pd
import numpy as np
from pathlib import Path

# make data_path pathlib-friendly and resolve relative to this file
data_path = Path("../../data/llm_patients.csv")
if not data_path.is_absolute():
    # resolve relative to the repository/code file location (works on Windows)
    data_path = (Path(__file__).resolve().parent / data_path).resolve()



llm_patients = pd.read_csv(data_path, sep="|")

def get_random_patient():
    random_idx = np.random.randint(0, len(llm_patients))
    patient_data = llm_patients.iloc[random_idx]
    return {key: patient_data[key] for key in llm_patients.columns}



if __name__ == "__main__":
    patient = get_random_patient()
    # print(patient["Full"])
    print(patient['Medical Conditions'])
    print(patient)
