# supervisor for the interaction loop
# %%
import pickle
from investigator import Investigator
from rep_patient_analysis import distance_rep_patient

symptoms_func = distance_rep_patient

def ask_patient(question) -> dict:
    disorder = "Dissociative Identity Disorder"
    code = "F44.81"
    system_msg = {
            "role": "system",
            "content": f"""
            You are a patient being interviewed by a mental health medical investigator.
            You must simulate the symptoms of {disorder}, as classified by ICD-10 code {code}.
            Answer the investigator's questions in a way that reflects the experiences and challenges associated with {disorder}.
            """

        }
    
    
    return 
INITIAL_QUESTION = "What brings you today?"
FRONT_EXPORT_PATH = "data/investigator.pkl"

def main():
    investigator = Investigator()
    question = INITIAL_QUESTION
    while True:
        print("Asking patient")
        response = ask_patient(question, investigator.conversation_history)
        investigator.update_conversation_history(response, role="patient")
    
        symptoms_score = symptoms_func(response["response"])
        print("Updating patient representation")
        investigator.update_patient_representation(symptoms_score)
        # TODO update clinical reprot
        # investigator.update_clinical_report()

        instruction =  investigator.generate_instruction()
        question = 

        print("Investigator instruction:", instruction)

        with open(FRONT_EXPORT_PATH, "wb") as stream:
            pickle.dump(investigator, stream)
        print(f"Exported investigator to {FRONT_EXPORT_PATH}")



if __name__ == '__main__':
    main()

    