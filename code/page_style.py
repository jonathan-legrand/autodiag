
import streamlit as st

import pandas as pd
from pathlib import Path

import plotly.express as px



root_folder = Path('C:/Users/Sophie/Documents/Hack1robo/autodiag/')

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

image_url = "https://via.placeholder.com/100"

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

    
def write_info(df) : 
    lines = []
    for category, content in df.items():
        if isinstance(content, list):
            content = ", ".join(content)
        lines.append(f"<strong>{category}</strong>: {content}")
    return lines