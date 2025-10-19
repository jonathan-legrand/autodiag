
import streamlit as st
from os.path import basename, normpath, isfile, dirname, isdir
import sys
import re
import pandas as pd
from pathlib import Path
import time
import plotly.express as px



root_folder = Path('C:/Users/Sophie/Documents/Hack1robo/autodiag/')

st.markdown(
    """
    <style>  
    /* Supprimer les marges/paddings latéraux et forcer largeur à 100% */
    .css-18e3th9,  /* container principal */
    .css-1d391kg,  /* autre container possible */
    .block-container {
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



### insert real values
recap = ['Patient is sad', 'Patient hates their mum']
patient_info = {'Name' : 'Roger', 'Age' : 55, 'Sex': 'Male', 'Clinical history' : ['Diabetic', 'Epileptic']}
diagnosis_proba = pd.read_csv(root_folder / 'data/sample_proba.csv')



col_info, col_diag = st.columns(2)

with col_info : 
    with st.container(border = False, width = 500, height = 100) :
     # Deux colonnes : image à gauche, infos à droite
        col_img, col_info_text = st.columns([1, 3])  # Ratio 1:3

        with col_img:
            st.image("https://via.placeholder.com/100", width=100)  # Image par défaut

        with col_info_text:
            lines = []
            for category, contenu in patient_info.items():
                if isinstance(contenu, list):
                    contenu = ", ".join(contenu)
                lines.append(f"<strong>{category}</strong>: {contenu}")
    
        # Assemble les lignes avec des <br> HTML
        joined_lines = "<br>".join(lines)

        # Injecte du style CSS + contenu
        st.markdown("""
            <style>
                .big-font {
                    font-size: 15px !important;
                    line-height: 1.2;
                }
            </style>
        """, unsafe_allow_html=True)

        # Affiche le texte avec la classe CSS
        st.markdown(f'<p class="big-font">{joined_lines}</p>', unsafe_allow_html=True)

    with st.container(border = True) : 
        st.markdown('**Interview report**')
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
    # Ajout d'une colonne pour les couleurs personnalisées
    colors = ["#F8C8DC", "#A8DADC", "#CFFFE5", "#FFF3B0", "#DCC6E0"]
    diagnosis_proba['color'] = colors

    # Création du bar chart avec barres horizontales
    fig = px.bar(
        diagnosis_proba,
        x='disorder',
        y='symptome',
        orientation='h',
        color='symptome',
        color_discrete_sequence=colors,
        height=500
    )

    # Suppression de la légende si tu ne veux pas de doublon
    fig.update_layout(showlegend=False)

    # Affichage dans Streamlit
    st.plotly_chart(fig)



# Refresh every second
time.sleep(1)
st.rerun()
