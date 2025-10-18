# supervisor for the interaction loop
# %%
from investigator import Investigator
from rep_patient_analysis import distance_rep_patient

symptoms_func = distance_rep_patient

def ask_patient(question) -> dict:
    return {
        "response": "Some days I feel like I’m not the only one living my life, and it’s confusing trying to figure out who’s really in control."
    }

def main():
    investigator = Investigator()
    question = "What brings you today?"
    while True:
        response = ask_patient(question)
    
        symptoms_score = symptoms_func(response)
        investigator.update_patient_representation(symptoms_score)
        # TODO update clinical reprot
        # investigator.update_clinical_report()

        instruction =  investigator.generate_instruction()



if __name__ == '__main__':
    main()

    