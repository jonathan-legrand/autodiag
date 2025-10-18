
# %%
import numpy as np
import pandas as pd
from pathlib import Path

from functools import reduce

def concat_sentences(x, y):
    return x + ". " + y


class Investigator:
    def __init__(self, n_switch_cycles=5, data_path="../data/datalong.csv"):

        self.n_switch_cycles = n_switch_cycles
        self.iteration_counter = 0
        self.explore = True
        self.current_question = None

        # make data_path pathlib-friendly and resolve relative to this file
        data_path = Path(data_path)
        if not data_path.is_absolute():
            # resolve relative to the repository/code file location (works on Windows)
            data_path = (Path(__file__).resolve().parent / data_path).resolve()


        long_data = pd.read_csv(data_path, index_col=0)
        long_scores = long_data.copy()
        long_scores["score"] = np.zeros(shape=(len(long_data)))
        self.long_scores = long_scores
        self.long_data = long_data

        self.conversation_history = []
        self.conversation_summary = []


    # TODO
    def update_patient_representation(self):
        # append ton conv history
        # generate summary of actual known state of patient  
        pass    


    def update_patient_representation(self, new_scores):
        self.long_scores["score"] += new_scores["score"]
        self.iteration_counter += 1

        # first proxy: n cycles
        if self.iteration_counter > self.n_switch_cycles:
            self.explore = False

    def generate_instruction(self):
        if self.explore:
            return "Continue the conversation"
        most_important_disease = self.long_scores.sort_values(
            by="symptome", ascending=False
        ).loc[0, "code"]
        self.long_data[self.long_scores.code == most_important_disease]
        instructions = """
        "Ask a short question that explores as many of the following symptoms :

        """
        relevants_symptoms = reduce(concat_sentences, self.long_data[self.long_scores.code == "F60.2"].symptome)
        return instructions + relevants_symptoms

    def compute_score_distribution(self):
        sum_scores = self.long_scores.groupby("code").sum(numeric_only=True)
        sum_scores.sort_values(by="score", ascending=False, inplace=True)
        
        return sum_scores / self.iteration_counter

# %%
#investigator = Investigator()
#
#fake_update = investigator.long_scores.copy()
#rng = np.random.default_rng()
#fake_update["score"] = rng.normal(size=(len(fake_update)))
#
#print(investigator.long_scores[["code", "score"]].head())
#investigator.update_patient_representation(fake_update)
#print(investigator.long_scores[["code", "score"]].head())
## %%
#investigator.explore = False
#print(investigator.generate_instruction())
## %%
#investigator.compute_score_distribution()
#