import streamlit as st
from main import DialogueManager
import pandas as pd
from page_style import start_window, show_recap, plot_diagnosis, criteria_list, colors_chat, typewriter, define_color_sidebar



# Initialize session state
def init_session_state():
    if 'dialogue_manager' not in st.session_state:
        st.session_state.dialogue_manager = DialogueManager()


def app():

    
    init_session_state()

    investigator = st.session_state.dialogue_manager.investigator

    ### TO DO - real patient info 
    metadata = investigator.patient_metadata
    
    patient_info = {'Name': metadata['Full Name'], 'Age': metadata['Age'], 'Sex': metadata['Sex'], 
                    'Medications' : metadata['Medications']}
    

    start_window()



    if investigator.explore:
        col_info, col_diag = st.columns(2)

        with col_info:

            if len(investigator.clinical_report) > 0 :
                summary = investigator.clinical_report[-1]
            else : 
                summary = ''

            show_recap(patient_info, summary, n = investigator.iteration_counter)

            # Question container
            with st.container(border=True):
                st.markdown('**Suggested question:**')
                st.markdown(investigator.suggested_question)

                if st.button("**Ask next question**", type='primary'):
                    result = st.session_state.dialogue_manager.process_interaction()
                    st.rerun()
            
            # st.write(investigator.diagnose())

                
        # Diagnosis probability chart
        if investigator.iteration_counter > 0 : 
            with col_diag:

                diagnosis_proba = investigator.compute_score_distribution()
                if isinstance(diagnosis_proba, pd.DataFrame):

                    # Création du bar chart avec barres horizontales
                    plot_diagnosis(diagnosis_proba)


    else:
        disorder, symptoms =  investigator.diagnose()
        symptoms = list(set(list(symptoms)))

        st.session_state.setdefault("step", 1)
        st.session_state.setdefault("diag_result", '')

        # Étape 1
        if st.session_state.step == 1:
            with st.form(disorder, border = False):
                st.write(f'Confirm symptoms for **{disorder}**')
                c = [st.checkbox(s, key = f'{disorder} {s} {st.session_state.step}') for s in symptoms]
                submit1 = st.form_submit_button("**submit 1**", key = f'submit 1 {disorder}', type = 'primary')
                if submit1 :
                    if len(symptoms) >= investigator.min_symptoms : 
                        st.session_state.enough1 = sum(c) >= investigator.min_symptoms
                    else : 
                        st.session_state.enough1 = 1
                    st.session_state.step = 2


        # Étape 2 ou message selon résultat
        elif st.session_state.step == 2:
            if st.session_state.enough1:
                with st.form(f"criteria {disorder}", border = False):
                    d = [st.checkbox(c, key = f'{disorder} {c} {st.session_state.step}') for c in criteria_list]
                    if st.form_submit_button("**submit 2**", key = f'submit 2 {disorder}', type = 'primary'):
                        st.session_state.result = "success" if sum(d) == len(d) else "fail"
                        st.session_state.step = 3
            else: 
                st.write(f'{disorder} was not confirmed by diagnosis')

        
        # Résultat final
        elif st.session_state.step == 3:
            if st.session_state.result == "success" :
                
                st.success(f"✅ Patient has **{disorder}**") 
    
            else: 
                st.error(f'**{disorder}** was not confirmed by diagnosis]')

    with st.sidebar : 
        define_color_sidebar()
        st.markdown(':red[**Simulation**]')
        st.markdown(f'**Disorder**: {'; '.join(investigator.actual_diagnoses)}')
        with st.container(): 
            for e, element in enumerate(investigator.conversation_history) : 
                with st.container() : 
                    st.markdown(f':{colors_chat[element["role"]]}[**{element["role"]}**]')
                with st.container(border = True) : 
                    if e >= len(investigator.conversation_history) - 2 and investigator.explore : 
                        speed = 5
                        typewriter(text=f'*{element["content"]}*', speed=speed)
                    else :
                        st.write(f"*{element['content']}*")
            


if __name__ == "__main__":
    app()