import streamlit as st
from main import DialogueManager
import pandas as pd
from page_style import start_window, show_recap, plot_diagnosis, criteria_list

# Initialize session state
def init_session_state():
    if 'dialogue_manager' not in st.session_state:
        st.session_state.dialogue_manager = DialogueManager()


def app():
    tab_main, tab_historic = st.tabs(['Main', 'Historic'])
    
    init_session_state()

    investigator = st.session_state.dialogue_manager.investigator

    ### TO DO - real patient info 
    metadata = investigator.patient_metadata
    
    patient_info = {'Name': metadata['Full Name'], 'Age': metadata['Age'], 'Sex': metadata['Sex'], 
                    'Medications' : metadata['Medications']}
    


    with tab_main : 
        start_window()
    
        
        
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
            symptoms = list(symptoms)

            with st.form(disorder):
                st.write(disorder)

                symptoms_checkboxes = []
                for s in range(len(symptoms)) :
                    symptoms_checkboxes.append(st.checkbox(symptoms[s], key = f'{symptoms} {s}'))
                
                submitted = st.form_submit_button("Submit", key = disorder)
                
                if not submitted:
                    st.stop()
            
            symptoms_bool = symptoms_checkboxes.copy()


            if sum(symptoms_bool) >= investigator.min_symptoms :  



                # with st.container():
                st.write('Validation criteria')
                
                criteria_bool = [1 for _ in criteria_list]

                # for s in range(len(criteria_list)) :
                #     criteria_bool[s] = st.checkbox(criteria_list[s], key = f'validation {disorder} {s}')

                validate = st.button('Submit', key = f'button validation {disorder}')
                
                if not validate : 
                    st.stop()

                st.write(sum(criteria_bool), len(criteria_bool))
                if sum(criteria_bool) == len(criteria_bool) : 
                    investigator.update_disease(disorder, 1)
                    st.write('YAY you are sick')

                else :
                    investigator.update_disease(disorder, 0)
        
            else : 
                investigator.update_disease(disorder, 0)

    with tab_historic : 
        st.write(investigator.conversation_history)



if __name__ == "__main__":
    app()