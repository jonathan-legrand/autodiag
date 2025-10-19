
import streamlit as st

import pandas as pd
from pathlib import Path

import plotly.express as px

import time

criteria_list = ['Do these symptoms last longer than 2 weeks?', 'Do these symptoms have an impact on private and professional life?', 'Do these symptoms cause significant suffering?']

init_style = """
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
    """

def start_window() : 
    st.markdown(init_style,unsafe_allow_html=True)
    st.title("Artificial Diagnosis")

image_url = "https://via.placeholder.com/100"

def write_info(df) : 
    lines = []
    for category, content in df.items():
        if isinstance(content, list):
            content = ", ".join(content)
        lines.append(f"<strong>{category}</strong>: {content}")
    return lines

def show_recap(patient_info, summary) : 
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
        for recap in summary:
            st.markdown(f'- {recap}')


colors_plot = ["#F8C8DC", "#A8DADC", "#CFFFE5", "#FFF3B0", "#DCC6E0"]


def plot_diagnosis(diagnosis_proba):
    """
    Affiche un bar chart horizontal des scores de diagnostic dans Streamlit,
    avec des couleurs personnalisées.

    Args:
        diagnosis_proba (pd.DataFrame): DataFrame contenant les colonnes 'score' et 'disorder'.
                                        Une colonne 'color' est générée automatiquement.
    """

    diagnosis_proba = diagnosis_proba[:5]

    # Liste de couleurs personnalisées (autant que de lignes dans le DataFrame)
    custom_colors = ["#F8C8DC", "#A8DADC", "#CFFFE5", "#FFF3B0", "#DCC6E0"]

    # Créer le bar chart
    fig = px.bar(
        diagnosis_proba,
        x='score',
        y='disorder',
        orientation='h',
        color='disorder',
        color_discrete_sequence=custom_colors,
        height=500
    )
    # Retirer la légende
    fig.update_layout(showlegend=False)

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

colors_chat = {'clinician' : 'blue', 'patient' : 'red'}  # gris clair / bleu clair

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

