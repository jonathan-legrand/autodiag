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
    patient_data = llm_patients.iloc[random_idx,:]
    labels = patient_data["Medical Conditions"].split(", ")
    demographics = {key: patient_data[key] for key in llm_patients.columns if key != "Medical Conditions"}
    return labels, demographics

def get_patient_from_index(index: int):
    patient_data = llm_patients.iloc[index,:]
    labels = patient_data["Medical Conditions"].split(", ")
    demographics = {key: patient_data[key] for key in llm_patients.columns if key != "Medical Conditions"}
    return labels, demographics

def get_patient_from_disorder(disorder: str):
    filtered_patients = llm_patients[llm_patients["Medical Conditions"].str.contains(disorder, na=False)]
    if len(filtered_patients) == 0:
        raise ValueError(f"No patients found with disorder: {disorder}")
    random_idx = np.random.randint(0, len(filtered_patients))
    patient_data = filtered_patients.iloc[random_idx,:]
    labels = patient_data["Medical Conditions"].split(", ")
    demographics = {key: patient_data[key] for key in llm_patients.columns if key != "Medical Conditions"}
    return labels, demographics


if __name__ == "__main__":
    patient = get_random_patient()
    # print(patient["Full"])
    print(patient['Medical Conditions'])
    print(patient)
