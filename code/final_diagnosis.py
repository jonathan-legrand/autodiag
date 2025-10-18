from pathlib import Path
import pandas as pd

disorders_path = Path('../data/list_disorder.csv')

if not disorders_path.is_absolute():
            # resolve relative to the repository/code file location (works on Windows)
            symptoms_embeddings_path = (Path(__file__).resolve().parent / disorders_path).resolve()

disorders_list = pd.read_csv(disorders_path)

def initial_disorder() :
    return({disorder : -1 for disorder in disorders_list})