import streamlit as st
from main import DialogueManager
from pathlib import Path
import pickle
import pandas as pd
# from front import root_folder

# Initialize session state
def init_session_state():
    if 'dialogue_manager' not in st.session_state:
        st.session_state.dialogue_manager = DialogueManager()
        # Save initial state
        # with open(root_folder / 'data' / 'investigator.pkl', 'wb') as fp:
        #     pickle.dump(st.session_state.dialogue_manager.investigator, fp)

def app():
    st.title("Medical Interview System")
    init_session_state()

    # Load styling from front.py
    st.markdown(
        """
        <style>  
        .css-18e3th9, .css-1d391kg, .block-container {
            padding-left: 75px !important;
            padding-right: 75px !important;
            margin-left: 20px !important;
            margin-right: 20px !important;
            max-width: 100% !important;
            width: 100% !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    investigator = st.session_state.dialogue_manager.investigator
    patient_info = {'Name': 'Roger', 'Age': 55, 'Sex': 'Male', 
                   'Clinical history': ['Diabetic', 'Epileptic']}

    if investigator.explore:
        col_info, col_diag = st.columns(2)

        with col_info:
            # Patient info container
            with st.container(border=False):
                col_img, col_info_text = st.columns([1, 3])
                with col_img:
                    st.image("https://via.placeholder.com/100", width=100)
                with col_info_text:
                    lines = []
                    for category, content in patient_info.items():
                        if isinstance(content, list):
                            content = ", ".join(content)
                        lines.append(f"<strong>{category}</strong>: {content}")
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
                    # # Save state after interaction
                    # with open(root_folder / 'data' / 'investigator.pkl', 'wb') as fp:
                    #     pickle.dump(investigator, fp)
                    st.rerun()

                st.markdown(investigator.suggested_question)

        # Diagnosis probability chart
        with col_diag:
            diagnosis_proba = investigator.compute_score_distribution()
            if isinstance(diagnosis_proba, pd.DataFrame):
                diagnosis_proba = diagnosis_proba.sort_values(by='score', ascending=False)
                diagnosis_proba = diagnosis_proba[:5]
                st.bar_chart(
                    data=diagnosis_proba,
                    x='disorder',
                    y='score',
                    height=500
                )

    else:
        st.write('diagnosis')

if __name__ == "__main__":
    app()