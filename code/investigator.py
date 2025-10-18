
# %%
import numpy as np
import pandas as pd
from pathlib import Path

from functools import reduce

def concat_sentences(x, y):
    return x + ". " + y

def most_important(object) : 
    # TO DO need to check that most important disease was not already investigated as false 

    most_important_disease = object.long_scores.sort_values(
            by="score", ascending=False
        ).reset_index(drop=True).loc[0, "disorder"]
    most_important_symptoms = object.long_data[object.long_scores.disorder == most_important_disease].symptome

    return most_important_disease, most_important_symptoms


class Investigator:
    def __init__(self, n_switch_cycles=5, data_path="../data/datalong.csv"):

        self.n_switch_cycles = n_switch_cycles
        self.iteration_counter = 0
        self.explore = True
        self.current_question = None
        self.min_symptoms = 3
        self.patient_metadata = {

        }


        # init random patient from llm_patients db
        from patients.patient import get_random_patient
        labels, patient = get_random_patient()
        self.actual_diagnoses = labels
        # print(self.patient_metadata)
        print("Actual diagnoses:", self.actual_diagnoses)
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
        self.system_conversation_history = []


    @property
    def suggested_question(self):
        return self.conversation_history[-1]["content"]

    def update_conversation_history(self, message: str, role: str):
        self.conversation_history.append({"role": role, "content": message})

    def update_patient_representation(self, new_scores):
        self.long_scores["score"] += new_scores["score"]
        self.iteration_counter += 1

        # first proxy: n cycles
        if self.iteration_counter > self.n_switch_cycles:
            self.explore = False

    def generate_instruction(self):
        most_important_disease, most_important_symptoms = most_important(self)
        
        relevant_symptoms = reduce(
            concat_sentences, most_important_symptoms
        )

        # choose prompt text based on mode (do not return early)
        if self.explore:
            prompt_text = (
                "Continue the conversation with the patient to explore their symptoms. "
                f"Focus on gathering information about the patient's symptoms. "
                "Ask concise and relevant questions to better understand the patient's condition."
            )
        else:
            prompt_text = (
                f"Based on the patient's responses, it appears that the most relevant diagnosis is "
                f"{most_important_disease}. To confirm this diagnosis, ask questions which are informative about the "
                f"following symptoms: {relevant_symptoms}. Your goal is to gather specific information that "
                "will help validate or refute this diagnosis."
            )

        # build chat-style messages: include a system message and the conversation + current instruction
        system_msg = {
            "role": "system",
            "content": "You are a concise mental health medical interviewer. Ask short, relevant questions to gather patient information."
        }

        # preserve conversation_history if it contains role/content dicts, otherwise join strings
        if self.conversation_history and isinstance(self.conversation_history[0], dict) and "role" in self.conversation_history[0]:
            history_msgs = self.conversation_history[:]  # already message dicts
        else:
            history_text = "\n".join(self.conversation_history) if self.conversation_history else ""
            history_msgs = [{"role": "user", "content": history_text}] if history_text else []

        instruction_msg = {"role": "user", "content": prompt_text}

        return [system_msg] + history_msgs + [instruction_msg]

    def compute_score_distribution(self):
        sum_scores = self.long_scores.groupby("disorder").sum(numeric_only=True).reset_index()
        sum_scores.sort_values(by="score", ascending=False, inplace=True)
        sum_scores["score"] = sum_scores["score"] / self.iteration_counter
        
        return sum_scores
    
    def diagnose(self) : 
        return most_important(self)
        
        


# %%
#investigator = Investigator()
## %%
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
#
#a, b = investigator.generate_instruction()
#print(a)
## %%
#investigator.compute_score_distribution()

# %%
