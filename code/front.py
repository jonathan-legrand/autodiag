import streamlit as st
from main import DialogueManager
import pandas as pd
from page_style import init_style, image_url, plot_diagnosis, write_info

# Initialize session state
def init_session_state():
    if 'dialogue_manager' not in st.session_state:
        st.session_state.dialogue_manager = DialogueManager()


def app():
    st.markdown(init_style,unsafe_allow_html=True)
    st.title("Medical Interview System")
    init_session_state()

    investigator = st.session_state.dialogue_manager.investigator

    ### TO DO - real patient info 
    patient_info = {'Name': 'Roger', 'Age': 55, 'Sex': 'Male', 
                   'Clinical history': ['Diabetic', 'Epileptic']}

    if investigator.explore:
        col_info, col_diag = st.columns(2)

        with col_info:
            # Patient info container
            with st.container(border=False):
                col_img, col_info_text = st.columns([1, 3])
                with col_img:
                    st.image(image_url, width=100)
                with col_info_text:
                    lines = write_info(patient_info)
                    
                    st.markdown(
                        f'<p class="big-font">{"<br>".join(lines)}</p>', 
                        unsafe_allow_html=True
                    )

            # Interview report container
            with st.container(border=True):
                st.markdown('**Interview report**')
                for recap in investigator.conversation_summary:
                    st.markdown(f'- {recap}')

            # Question container
            with st.container(border=True):
                st.markdown('**Suggested question:**')
                if st.button("Ask next question"):
                    result = st.session_state.dialogue_manager.process_interaction()
                    st.rerun()

                st.markdown(investigator.suggested_question)

        # Diagnosis probability chart
        with col_diag:
            diagnosis_proba = investigator.compute_score_distribution()
            if isinstance(diagnosis_proba, pd.DataFrame):

                # Création du bar chart avec barres horizontales
                plot_diagnosis(diagnosis_proba)


    else:
        st.write('diagnosis')

if __name__ == "__main__":
    app()