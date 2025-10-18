import streamlit as st
from main import DialogueManager
import pandas as pd
from page_style import start_window, show_recap, plot_diagnosis, check_criteria, criteria_list

# Initialize session state
def init_session_state():
    if 'dialogue_manager' not in st.session_state:
        st.session_state.dialogue_manager = DialogueManager()


def app():
    start_window()
    
    init_session_state()

    investigator = st.session_state.dialogue_manager.investigator

    ### TO DO - real patient info 
    metadata = investigator.patient_metadata
    
    patient_info = {'Name': metadata['Full Name'], 'Age': metadata['Age'], 'Sex': metadata['Sex'], 
                    'Medications' : metadata['Medications']}
    

    
    if investigator.explore:
        col_info, col_diag = st.columns(2)

        with col_info:

            summary = investigator.conversation_summary

            show_recap(patient_info, summary)

            # Question container
            with st.container(border=True):
                st.markdown('**Suggested question:**')
                st.markdown(investigator.suggested_question)

                if st.button("Ask next question"):
                    result = st.session_state.dialogue_manager.process_interaction()
                    st.rerun()

                
        # Diagnosis probability chart
        if investigator.iteration_counter > 0 : 
            with col_diag:

                diagnosis_proba = investigator.compute_score_distribution()
                if isinstance(diagnosis_proba, pd.DataFrame):

                    # Création du bar chart avec barres horizontales
                    plot_diagnosis(diagnosis_proba)


    else:
        disorder, symptoms = investigator.diagnose()
        symptoms_bool = check_criteria(disorder, symptoms)

        if sum(symptoms_bool) >= investigator.min_symptoms :  

            criteria_bool = check_criteria('Diagnosis criteria', criteria_list)
            if sum(criteria_bool) == len(criteria_bool) : 
                st.write('YAY you are sick')


if __name__ == "__main__":
    app()