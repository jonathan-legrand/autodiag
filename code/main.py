# supervisor for the interaction loop
# %%
import pickle
from investigator import Investigator
from rep_patient_analysis import distance_rep_patient
from llm_query import call_api

symptoms_func = distance_rep_patient

def ask_patient(question, conv_history: list[dict]) -> dict:
    disorder = "Dissociative Identity Disorder"
    code = "F44.81"
    system_msg = [
        {
            "role": "system",
            "content": f"""
            You are a patient being interviewed by a mental health medical investigator.
            You must simulate the symptoms of {disorder}, as classified by ICD-10 code {code}.
            Answer the investigator's questions in a way that reflects the experiences and challenges associated with {disorder}.
            Do not acknowledge symptoms that are not related to your disorder.
            """
            }
            ]
    
    question_msg = [{"role": "assistant", "content": question}]

    response = call_api(system_msg + conv_history + question_msg, role="patient")
    
    return response

INITIAL_QUESTION = "What brings you today?"
FRONT_EXPORT_PATH = "data/investigator.pkl"
class DialogueManager:
    def __init__(self):
        self.investigator = Investigator()
        self.question = INITIAL_QUESTION
        self.investigator.update_conversation_history(self.question, role="clinician")
    
    def process_interaction(self):
        """Single turn of dialogue"""
        response = ask_patient(self.question, self.investigator.conversation_history)
        self.investigator.update_conversation_history(response, role="patient")
        
        symptoms_score = symptoms_func(response)
        self.investigator.update_patient_representation(symptoms_score)
        
        instruction = self.investigator.generate_instruction()
        self.question = call_api(instruction, role="clinician")
        self.investigator.update_conversation_history(self.question, role="clinician")
        
        # # Save state
        # with open(FRONT_EXPORT_PATH, "wb") as stream:
        #     pickle.dump(self.investigator, stream)
            
        return {
            "response": response,
            "next_question": self.question,
            "diagnosis_proba": self.investigator.compute_score_distribution()
        }

# Remove the main() function as it will be controlled by Streamlit