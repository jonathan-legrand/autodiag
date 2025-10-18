
import streamlit as st
from os.path import basename, normpath, isfile, dirname, isdir
import sys
import re
import pandas as pd
from pathlib import Path
import time
import pickle
from investigator import Investigator
import streamlit as st
from main import DialogueManager


def init_session_state():
    """Initialize session state variables"""
    if 'dialogue_manager' not in st.session_state:
        st.session_state.dialogue_manager = DialogueManager()
    if 'conversation_active' not in st.session_state:
        st.session_state.conversation_active = True

def app():
    st.title("Medical Dialogue System")
    
    init_session_state()
    
    # Display patient info
    with st.container():
        # ...existing patient info display code...
        pass
    
    # Display conversation history
    with st.container():
        for msg in st.session_state.dialogue_manager.investigator.conversation_history:
            role = msg["role"]
            content = msg["content"]
            if role == "clinician":
                st.write("👨‍⚕️ Doctor:", content)
            else:
                st.write("🤒 Patient:", content)
    
    # Control flow
    if st.session_state.conversation_active:
        if st.button("Continue Dialogue"):
            result = st.session_state.dialogue_manager.process_interaction()
            
            # Update display
            st.write("🤒 Patient:", result["response"])
            st.write("👨‍⚕️ Next question:", result["next_question"])
            
            # Show diagnosis probabilities
            st.subheader("Current Diagnosis Probabilities")
            st.bar_chart(result["diagnosis_proba"])
    
    # Add option to reset conversation
    if st.button("Reset Conversation"):
        st.session_state.dialogue_manager = DialogueManager()
        st.rerun()

if __name__ == "__main__":
    app()