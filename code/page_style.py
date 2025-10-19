
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
    st.markdown(
    "<h1 style='color:#7DBDFF; font-weight:800;'>Artificial Diagnosis</h1>",
    unsafe_allow_html=True
)

image_path = Path('../data/Icone_patient.png')

if not image_path.is_absolute():
    # resolve relative to the repository/code file location (works on Windows)
    image_path = (Path(__file__).resolve().parent / image_path).resolve()

def write_info(df) : 
    lines = []
    for category, content in df.items():
        if isinstance(content, list):
            content = ", ".join(content)
        lines.append(f"<strong>{category}</strong>: {content}")
    return lines

def show_recap(patient_info, summary, n = 0) : 
    # Patient info container
    with st.container(border=False):
        col_img, col_info_text = st.columns([1, 3])
        with col_img:
            st.image(image_path, width=100)
        with col_info_text:
            lines = write_info(patient_info)
            
            st.markdown(
                f'<p class="big-font">{"<br>".join(lines)}</p>', 
                unsafe_allow_html=True
            )

    if n > 0 : 

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
        height=500,
        range_x = [0,1.05]
    )
    # Retirer la légende
    fig.update_layout(showlegend=False, 
    xaxis = dict(
        tickmode = 'array',
        tickvals = [0,0.25,0.5,0.75,1],
    )
)
    fig.update_traces(width=0.5)

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

colors_chat = {'clinician' : 'blue', 'patient' : 'red'}  # gris clair / bleu clair


def define_color_sidebar() : 
    st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #fdfeffff;
    }
</style>
""", unsafe_allow_html=True)

def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)


