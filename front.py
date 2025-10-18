
import streamlit as st
from os.path import basename, normpath, isfile, dirname, isdir
import sys
import re
import pandas as pd
from pathlib import Path

root_folder = Path('C:/Users/Sophie/Documents/Hack1robo/autodiag/')

st.markdown(
    """
    <style>
    /* Supprimer les marges/paddings latéraux et forcer largeur à 100% */
    .css-18e3th9,  /* container principal */
    .css-1d391kg,  /* autre container possible */
    .block-container {
        padding-left: 2 !important;
        padding-right: 2 !important;
        margin-left: 2 !important;
        margin-right: 2 !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align: center;
        font-size: 48px;  
        margin-top: 10px; 
        margin-bottom: 20px; 
        '>Autodiag</h1>
    """,
    unsafe_allow_html=True
)



### insert real values
recap = ['Patient is sad', 'Patient hates their mum']
patient_info = {'Name' : 'Roger', 'Age' : 55, 'Sex': 'Male', 'Previous diagnostic': [], 'Clinical history' : ['Diabetic', 'Epileptic']}
diagnosis_proba = pd.read_csv(root_folder / 'data/sample_proba.csv')



col_info, col_discussion, col_diag = st.columns([1,2,3])

with col_info : 

    with st.container(border = True) : 
        st.markdown('**Patient informations**')
        for category in patient_info.keys():
            contenu = patient_info[category]
            if type(contenu) == list : 
                contenu = ", ".join(contenu)
            
            st.markdown(f'- {category} : {contenu}')

    with st.container(border = True) : 
        st.markdown('**Summary**')
        for recap_i in recap : 
            st.markdown(f'- {recap_i}')
with col_discussion: 
    with st.container(border = True) : 
        st.markdown('**Suggested question:**')

        ### INSERT REAL VALUES
        st.markdown('Hi, what brings you here today?')

with col_diag : 
    diagnosis_proba = diagnosis_proba.sort_values(by = 'symptome', ascending=False)
    diagnosis_proba = diagnosis_proba[diagnosis_proba.index < 5]
    # diagnosis_proba = diagnosis_proba.drop(labels =['index'])
    st.bar_chart(diagnosis_proba, horizontal = True, x = 'disorder', y = 'symptome', height = 500)
    
