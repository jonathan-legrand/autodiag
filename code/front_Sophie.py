
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
import plotly.graph_objects as go

# root_folder = Path('C:/Users/achil/Documents/autodiag/')
root_folder = Path('C:/Users/Sophie/Desktop/Hack1robo/autodiag/')

chemin_logo_footer = '/data/logo-diagnostic-artificiel-3.png'
# Simuler une "base de données" utilisateur
USERS = {
    "sophie": "monmotdepasse",
    "admin": "admin123"
}

def login():
    st.columns(3)[1].image(f'{root_folder}/data/logo-diagnostic-artificiel-5.png', width = 800)

    username = st.columns(5)[2].text_input("email")
    password = st.columns(5)[2].text_input("Password", type="password")

    
    if st.columns(5)[2].button("Log in", key="button1", type = "primary"):

        if username in USERS and USERS[username] == password:
            st.success(f"Bienvenue {username} !")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

def main_app():
    st.title("Page principale")
    st.write(f"Bienvenue sur l'application, {st.session_state['username']} !")

    if st.button("Se déconnecter"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""

    if st.session_state["logged_in"]:
        main_app()
    else:
        login()

if __name__ == "__main__":
    main()



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

investigator.explore = False
diagnosis = False

report = "test report"

recap = investigator.conversation_summary


patient_info = {'Name' : 'Roger', 'Age' : 55, 'Sex': 'Male', 'Clinical history' : ['Diabetic', 'Epileptic']}

diagnosis_proba = investigator.compute_score_distribution()
def plot_diagnosis_bar_chart(diagnosis_proba):
        """
        Affiche un bar chart horizontal des scores de diagnostic dans Streamlit,
        avec des couleurs personnalisées.

        Args:
            diagnosis_proba (pd.DataFrame): DataFrame contenant les colonnes 'score' et 'disorder'.
                                            Une colonne 'color' est générée automatiquement.
        """

        # Liste de couleurs personnalisées (autant que de lignes dans le DataFrame)
        custom_colors = ["#F8C8DC", "#A8DADC", "#CFFFE5", "#FFF3B0", "#DCC6E0"]

        # Ajouter une colonne 'color' (optionnel, uniquement si tu veux la conserver)
        # diagnosis_proba = diagnosis_proba.copy()
        # diagnosis_proba['color'] = custom_colors[:len(diagnosis_proba)]

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

st.write(investigator.explore)
st.write(diagnosis)

if investigator.explore : 

    col_info, col_diag = st.columns(2)

    with col_info : 
        with st.container(border = False, width = 500, height = 100) :
        # Deux colonnes : image à gauche, infos à droite
            col_img, col_info_text = st.columns([1, 3])  # Ratio 1:3

            with col_img:
                st.image(f'{root_folder}/data/Icone_Patient.png')

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
        
    
        # st.bar_chart(diagnosis_proba, horizontal = True, x = 'disorder', y = 'score', height = 500, sort = False)
        plot_diagnosis_bar_chart(diagnosis_proba)

        st.columns(5)[4].image(f'{root_folder}/data/logo-diagnostic-artificiel-3.png', width = 500)
elif diagnosis: 
    col_info, col_diag = st.columns(2)

    with col_info : 
        with st.container(border = False, width = 500, height = 100) :
        # Deux colonnes : image à gauche, infos à droite
            col_img, col_info_text = st.columns([1, 3])  # Ratio 1:3

            with col_img:
                st.image(f'{root_folder}/data/Icone_Patient.png')
    

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
    
    
    st.write("Disorder")
    
    with st.form("my_form"):
                
        checkbox_val = st.checkbox("Form checkbox", key = 0)
        checkbox_val1 = st.checkbox("Form checkbox", key = 1)
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write( "checkbox", checkbox_val, "checkbox1", checkbox_val1)

else : 
    col_info, col_diag = st.columns(2)

    with col_info : 
        with st.container(border = False, width = 500, height = 100) :
        # Deux colonnes : image à gauche, infos à droite
            col_img, col_info_text = st.columns([1, 3])  # Ratio 1:3

            with col_img:
                st.image(f'{root_folder}/data/Icone_Patient.png')

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

    with st.container(border = False) :
        st.markdown('<div style="text-align: center;font-size: 40px"><b>Report</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: center">{report}</div>', unsafe_allow_html=True)
    # Créer deux boutons côte à côte avec columns
    col1, col2 = st.columns(2)

    with col1:
        # Conteneur pour aligner le bouton à gauche
        st.markdown('<div style="text-align: left;">', unsafe_allow_html=True)
        if st.button("Download PDF"):
            st.success("PDF téléchargé ! (placeholder)")
        st.markdown('</div>', unsafe_allow_html=True)


    with col2:
        # Conteneur pour aligner le bouton à droite
        st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
        if st.button("Close the session"):
            st.warning("Session fermée ! (placeholder)")
        st.markdown('</div>', unsafe_allow_html=True)


def footer(chemin_logo_footer) :
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
    st.markdown(footer,unsafe_allow_html=True)
    st.columns(10)[9].image(f'{root_folder}{chemin_logo_footer}', width = 200)

  



# Refresh every second
time.sleep(1)
st.rerun()
count += 1