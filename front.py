
import streamlit as st
from os.path import basename, normpath, isfile, dirname, isdir
import sys
import re
import pandas as pd
from pathlib import Path

root_folder = Path('C:/Users/melina.scopin/autodiag/')

tab_main, tab_base = st.tabs(['Main', 'database'])

### insert real values
recap = ['Patient is sad', 'Patient hates their mum']
patient_info = {'Name' : 'Roger', 'Age' : 55, 'Sex': 'Male', 'Previous diagnostic': [], 'Clinical history' : ['Diabetic', 'Epileptic']}
diagnosis_proba = pd.read_csv(root_folder / 'data/sample_proba.csv')

with tab_main : 

    col_info, col_diag = st.columns(2)

    with col_info : 

        with st.container(border = True) : 
            st.markdown('**Patient information**')
            for category in patient_info.keys():
                contenu = patient_info[category]
                if type(contenu) == list : 
                    contenu = ", ".join(contenu)
                
                st.markdown(f'- {category} : {contenu}')

        with st.container(border = True) : 
            st.markdown('**Summary**')
            for recap_i in recap : 
                st.markdown(f'- {recap_i}')

        with st.container(border = True) : 
            st.markdown('**Suggested question:**')

            ### INSERT REAL VALUES
            st.markdown('Hi, what brings you here today?')

    with col_diag : 
        diagnosis_proba = diagnosis_proba.sort_values(by = 'symptome', ascending=False)
        diagnosis_proba = diagnosis_proba[diagnosis_proba.index < 5]
        # diagnosis_proba = diagnosis_proba.drop(labels =['index'])
        st.bar_chart(diagnosis_proba, horizontal = True, x = 'disorder', y = 'symptome', height = 500)
        

        
with tab_base :
    st.write('Hello')