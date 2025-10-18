
import streamlit as st
from os.path import basename, normpath, isfile, dirname, isdir
import sys
import re
import pandas as pd
from pathlib import Path
import time
import pickle
from investigator import Investigator
import plotly.express as px


# root_folder = Path('C:/Users/achil/Documents/autodiag/')
root_folder = Path('C:/Users/Sophie/Documents/Hack1robo/autodiag/')

def turn_true(go) : 
    go = True
    return go

count = 0

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




with open(root_folder / 'data' / 'investigator.pkl', 'rb') as fp:
    investigator  = pickle.load(fp)

investigator.explore = True

recap = investigator.conversation_summary


patient_info = {'Name' : 'Roger', 'Age' : 55, 'Sex': 'Male', 'Clinical history' : ['Diabetic', 'Epileptic']}

diagnosis_proba = investigator.compute_score_distribution()

st.write(investigator.explore)
if investigator.explore : 

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

                go = False

                st.markdown(investigator.suggested_question)

                # st.button('validate question', key = f'question_{count}', on_click = turn_true(go))

                if go :
                    # see how we move on 
                    pass
            
    with col_diag : 
        # st.write(diagnosis_proba)
        diagnosis_proba = diagnosis_proba.sort_values(by = 'score', ascending=False)
        diagnosis_proba = diagnosis_proba[:5]
        # st.write(diagnosis_proba.columns)
        # Ajout d'une colonne pour les couleurs personnalisées
        colors = ["#F8C8DC", "#A8DADC", "#CFFFE5", "#FFF3B0", "#DCC6E0"]
        diagnosis_proba['color'] = colors

        # Création du bar chart avec barres horizontales
        fig = px.bar(
            diagnosis_proba,
            x='disorder',
            y='score',
            orientation='h',
            color='score',
            color_discrete_sequence=colors,
            height=500
        )

        # Suppression de la légende si tu ne veux pas de doublon
        fig.update_layout(showlegend=False)

        # Affichage dans Streamlit
        st.plotly_chart(fig)
        # st.bar_chart(diagnosis_proba, horizontal = True, x = 'disorder', y = 'score', height = 500, sort = False)
else : 
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
    with st.form("my_form"):
        st.write("Disorder")
        
        checkbox_val = st.checkbox("Form checkbox", key = 0)
        checkbox_val1 = st.checkbox("Form checkbox", key = 1)
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write( "checkbox", checkbox_val, "checkbox1", checkbox_val1)
st.write("Outside the form")


# Refresh every second
time.sleep(1)
st.rerun()
count += 1