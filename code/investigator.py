# %%
import numpy as np
import pandas as pd

rng = np.random.default_rng()
long_desc = pd.read_csv("../data/datalong.csv", index_col=0)
# %%

long_scores = long_desc.copy()
long_scores["symptome"] = rng.normal(size=(len(long_desc)))
# %%
import seaborn as sns
import matplotlib.pyplot as plt

sorted_disorders = long_scores.groupby("disorder").sum(numeric_only=True).sort_values(
    by="symptome", ascending=False
)
most_likely_disorder = sorted_disorders.index[0]

# %%
res = long_desc[long_desc.code == most_likely_disorder]
res
# %%

class Investigator:
    def __init__(self, n_switch_cycles=5):
        self.n_switch_cycles = n_switch_cycles
        self.iteration_counter = 0
        self.explore = True
        self.long_data = pd.read_csv("data/datalong.csv", index_col=0)
        long_scores = self.long_data.copy()
        long_scores["score"] = np.zeros(size=(len(long_desc)))
        self.long_scores = long_scores

        self.conversation_history = []
        self.conversation_summary = []

    # TODO
    def update_patient_representation(self):
        # append ton conv history
        # generate summary of actual known state of patient  
        pass    


    def update_patient_representation(self, new_scores):
        self.long_scores += new_scores
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
        self.long_data[long_scores.code == most_important_disease]
        ## Extract most important symptom
        # Explore symptoms from same pathology
        pass

    def compute_score_distribution(self):
        return self.long_scores.groupby("code").sum(numeric_only=True) / self.iteration_counter
