import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Intelligent Manager MVP", layout="wide")

st.title("Intelligent Manager (MVP texte incrémental)")
st.write("Step 1 : Input des tâches/éléments de travail et génération du prompt LLM")

# --- Initialisation de la session ---
if "elements" not in st.session_state:
    st.session_state.elements = []  # Liste des éléments initiaux
if "actualisations" not in st.session_state:
    st.session_state.actualisations = []  # Liste des ajouts post-envoi
if "llm_output" not in st.session_state:
    st.session_state.llm_output = ""  # Texte collé depuis LLM

# --- Step 1 : Input des éléments ---
st.subheader("Ajouter de nouveaux éléments / actualisations")
cols = st.columns([6,1])
new_input = cols[0].text_input("Nouvel élément", key="new_input")
add_button = cols[1].button("➕ Ajouter")

if add_button and new_input.strip() != "":
    # Ajout dans éléments initiaux si LLM pas encore rempli, sinon dans actualisations
    if not st.session_state.elements or st.session_state.llm_output == "":
        st.session_state.elements.append(new_input.strip())
    else:
        st.session_state.actualisations.append(new_input.strip())
    # Pas de st.experimental_rerun() : Streamlit va gérer l'affichage naturellement

# --- Affichage des éléments ---
st.subheader("Éléments actuels")
with st.expander("Step 1 : éléments initiaux"):
    for idx, el in enumerate(st.session_state.elements, 1):
        st.write(f"{idx}. {el}")

if st.session_state.actualisations:
    with st.expander("Actualisations / ajouts après premier envoi"):
        for idx, el in enumerate(st.session_state.actualisations, 1):
            st.write(f"{idx}. {el}")

# --- Step 2 : Prompt généré pour LLM ---
st.subheader("Prompt généré pour LLM")
prompt_text = "Voici tous les éléments à traiter :\n"
for idx, el in enumerate(st.session_state.elements, 1):
    prompt_text += f"Sujet {idx} : {el}\n"
if st.session_state.actualisations:
    prompt_text += "\n--- Actualisations ---\n"
    for idx, el in enumerate(st.session_state.actualisations, 1):
        prompt_text += f"Nouvel élément {idx} : {el}\n"

prompt_text += "\nObjectif : Décante les éléments en sous-steps, micro-actions, dépendances cachées et séquence optimale."

st.text_area("Prompt LLM (copypaste pour traitement)", prompt_text, height=300)

# --- Step 3 : Coller le retour LLM ---
st.subheader("Coller le retour du LLM ici")
llm_input = st.text_area("Retour LLM", st.session_state.llm_output, height=300)
update_button = st.button("💾 Mettre à jour LLM")

if update_button:
    st.session_state.llm_output = llm_input

# --- Historique / affichage final ---
st.subheader("Historique / Output complet")
st.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.text_area("LLM Output cumulatif", st.session_state.llm_output, height=300)
