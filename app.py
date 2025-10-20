import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Intelligent Manager MVP", layout="wide")
st.title("Intelligent Manager (MVP avec Prompts JSON)")

# --- Initialisation de la session ---
if "elements" not in st.session_state:
    st.session_state.elements = []
if "actualisations" not in st.session_state:
    st.session_state.actualisations = []
if "prepared_output" not in st.session_state:
    st.session_state.prepared_output = ""
if "final_output" not in st.session_state:
    st.session_state.final_output = ""

# --- Chargement des prompts depuis JSON ---
def load_prompt(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

preparation_prompt = load_prompt("prompts/preparation.json")
sequencage_prompt = load_prompt("prompts/sequencage.json")

# --- Step 1 : Input des éléments ---
st.subheader("Ajouter de nouveaux éléments / actualisations")
cols = st.columns([6,1])
new_input = cols[0].text_input("Nouvel élément", key="new_input")
add_button = cols[1].button("➕ Ajouter")

if add_button and new_input.strip() != "":
    if not st.session_state.elements or st.session_state.prepared_output == "":
        st.session_state.elements.append(new_input.strip())
    else:
        st.session_state.actualisations.append(new_input.strip())

# --- Affichage des éléments ---
st.subheader("Éléments cumulés")
with st.expander("Éléments initiaux"):
    for idx, el in enumerate(st.session_state.elements, 1):
        st.write(f"{idx}. {el}")

if st.session_state.actualisations:
    with st.expander("Actualisations / ajouts post-prep"):
        for idx, el in enumerate(st.session_state.actualisations, 1):
            st.write(f"{idx}. {el}")

# --- Prompt 1 : Préparation des éléments ---
st.subheader(f"Prompt 1 : {preparation_prompt['title']}")
elements_text = "\n".join(st.session_state.elements + st.session_state.actualisations)
prompt1_text = f"{preparation_prompt['instructions']}\n\nÉléments :\n{elements_text}\n\nFormat attendu :\n{preparation_prompt['output_format']}"
st.text_area("Prompt 1 LLM (copypaste)", prompt1_text, height=300)

# --- Zone pour coller output LLM préparation ---
st.subheader("Coller le retour LLM (Prompt 1)")
prepared_input = st.text_area("Retour LLM (préparation)", st.session_state.prepared_output, height=200)
update_prepared = st.button("💾 Mettre à jour préparation")

if update_prepared:
    st.session_state.prepared_output = prepared_input

# --- Prompt 2 : Séquençage et priorisation ---
st.subheader(f"Prompt 2 : {sequencage_prompt['title']}")
prompt2_text = f"{sequencage_prompt['instructions']}\n\nFiches à traiter :\n{st.session_state.prepared_output}\n\nFormat attendu :\n{sequencage_prompt['output_format']}"
st.text_area("Prompt 2 LLM (copypaste)", prompt2_text, height=300)

# --- Zone pour coller output LLM final ---
st.subheader("Coller le retour LLM (Prompt 2)")
final_input = st.text_area("Retour LLM final", st.session_state.final_output, height=200)
update_final = st.button("💾 Mettre à jour plan final")

if update_final:
    st.session_state.final_output = final_input

# --- Historique / affichage final ---
st.subheader("Historique / Output complet")
st.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.text_area("Output final LLM cumulatif", st.session_state.final_output, height=300)
