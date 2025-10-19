
import streamlit as st

import pandas as pd
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go

import time

logo_path = Path('../data/logo-diagnostic-artificiel-5.png')

if not logo_path.is_absolute():
    # resolve relative to the repository/code file location (works on Windows)
    logo_path = (Path(__file__).resolve().parent / logo_path).resolve()

logo_foot = Path('../data/logo-diagnostic-artificiel-3.png')

if not logo_foot.is_absolute():
    # resolve relative to the repository/code file location (works on Windows)
    logo_foot = (Path(__file__).resolve().parent / logo_foot).resolve()


def login_page() : 


    USERS = {
        "sophie": "monmotdepasse",
        "admin": "admin123"
    }
    
    st.columns(3)[1].image(logo_path, width = 800)

    username = st.columns(5)[2].text_input("email")
    password = st.columns(5)[2].text_input("password", type="password")

    
    if st.columns(5)[2].button("log in", key="button1", type = "primary"):

        if username in USERS and USERS[username] == password:
            st.success(f"Welcome {username} !")
            time.sleep(1.5)
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Wrong user name or password.")

    

criteria_list = ['Have these symptoms occured for longer than 2 weeks?', 'Do these symptoms have an impact on the patient daily life?', 'Do these symptoms cause significant suffering?', 'Differential diagnosis: the symptoms are not explained by other conditions']

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
    col1, col2 = st.columns([1,2])
    with col1 :
        st.markdown(init_style,unsafe_allow_html=True)
        st.markdown(
        "<h1 style='color:#7DBDFF; font-weight:800;'>Diagnostic Artificiel</h1>",
        unsafe_allow_html=True)
    with col2 : 
        footer()    

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
        with st.container():
            st.markdown('**Interview report**')
            for recap in summary:
                st.markdown(f'- {recap}')


colors_plot = ["#F8C8DC", "#A8DADC", "#CFFFE5", "#FFF3B0", "#DCC6E0"]


def plot_diagnosis(diagnosis_proba):
    """
    Affiche un bar chart horizontal des scores de diagnostic dans Streamlit,
    avec des couleurs personnalisées et étiquettes sous chaque barre.

    Args:
        diagnosis_proba (pd.DataFrame): DataFrame contenant les colonnes 'score' et 'disorder'.
    """
    diagnosis_proba = diagnosis_proba[:5]

    # Liste de couleurs personnalisées (autant que de lignes dans le DataFrame)
    custom_colors = ["#F8C8DC", "#A8DADC", "#CFFFE5", "#FFF3B0", "#DCC6E0"]

    # On crée la figure avec Plotly Express
    fig_px = px.bar(
    diagnosis_proba,
    x='score',
    y='disorder',
    orientation='h',
    color='disorder',
    color_discrete_sequence=custom_colors,
    range_x=[0, 1.05],
    height=500,
    )

    # Crée une figure vide
    fig = go.Figure()

    # Ajoute toutes les traces de fig_px à la nouvelle figure fig
    for trace in fig_px.data:
        fig.add_trace(trace)

    # Copie aussi la mise en page
    fig.update_layout(fig_px.layout)
    fig.update_yaxes(showticklabels=False)

    # Retirer la légende
    fig.update_layout(showlegend=False)

    # Ajuster ticks de l'axe X
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 0.25, 0.5, 0.75, 1],
        ),
        yaxis=dict(
            title ='',
        ),
        margin=dict(l=140, r=20, t=20, b=80)  # marge basse plus grande pour texte sous barres
    )

    fig.update_traces(width=0.3)

    # Ajouter annotations (étiquettes sous chaque barre)
    for i, row in diagnosis_proba.iterrows():
        fig.add_annotation(
            x=0,  # position au milieu de la barre horizontalement
            y=row['disorder'],
            text=f"<b>{row['disorder']}</b>",  # texte = score avec 2 décimales
            showarrow=False,
            yshift=-30,  # décalage vers le bas (sous la barre)
            font=dict(size=14, color="grey"),
            align='left',
            xanchor='left',
        )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)




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


def footer() :
    footer="""<style>
    a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
    }

    a:hover,  a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    color: black;
    text-align: center;
    padding-bottom : 0px !important;
    padding-left: 0px !important;
    padding-right: 0px !important;
    margin-bottom: 0px ! important;
    margin-left: 0px !important;
    margin-right: 0px !important;
    }
    </style>
    """
    st.write('')
    st.markdown(footer,unsafe_allow_html=True)
    st.columns(5)[3].image(f'{logo_foot}', width = 200)