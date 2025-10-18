# supervisor for the interaction loop
# %%
import pickle
from investigator import Investigator
from rep_patient_analysis import distance_rep_patient

symptoms_func = distance_rep_patient

def ask_patient(question) -> dict:
    return {
        "question": question,
        "response": "Some days I feel like I’m not the only one living my life, and it’s confusing trying to figure out who’s really in control."
    }

INITIAL_QUESTION = "What brings you today?"
FRONT_EXPORT_PATH = "data/investigator.pkl"

def main():
    investigator = Investigator()
    question = INITIAL_QUESTION
    while True:
        print("Asking patient")
        response = ask_patient(question)
        investigator.conversation_history.append(response)
    
        symptoms_score = symptoms_func(response["response"])
        print("Updating patient representation")
        investigator.update_patient_representation(symptoms_score)
        # TODO update clinical reprot
        # investigator.update_clinical_report()

        instruction =  investigator.generate_instruction()

        print("Investigator instruction:", instruction)

        with open(FRONT_EXPORT_PATH, "wb") as stream:
            pickle.dump(investigator, stream)
        print(f"Exported investigator to {FRONT_EXPORT_PATH}")



if __name__ == '__main__':
    main()

    