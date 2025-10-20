import streamlit as st
import json
from datetime import datetime
import os

st.set_page_config(page_title="Intelligent Manager MVP", layout="wide")
st.title("Intelligent Manager (MVP : LLM actualisations)")

# --- Session state ---
for key in ["inputs", "llm_output"]:
    if key not in st.session_state:
        st.session_state[key] = []

# --- Chargement du prompt JSON ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "prompts.json"), "r") as f:
    prompts = json.load(f)

main_prompt = prompts["main_prompt"]

# --- Input continu ---
st.subheader("Ajouter un nouvel élément ou mise à jour (tâche / contrainte / modification)")
cols = st.columns([6,1])
new_input = cols[0].text_input("Nouvel input", key="new_input")
add_button = cols[1].button("➕ Ajouter")

if add_button and new_input.strip() != "":
    st.session_state.inputs.append(new_input.strip())

# --- Affichage cumulatif ---
st.subheader("Éléments cumulés")
for idx, el in enumerate(st.session_state.inputs, 1):
    st.write(f"{idx}. {el}")

# --- Génération du prompt LLM ---
st.subheader(f"Prompt LLM à copypaste")
inputs_text = "\n".join(st.session_state.inputs)
prompt_text = f"{main_prompt['instructions']}\n\nÉléments bruts :\n{inputs_text}\n\nFormat attendu :\n{main_prompt['output_format']}"
st.text_area("Prompt LLM", prompt_text, height=350)

# --- Coller retour LLM ---
st.subheader("Coller le retour LLM (plan final consolidé)")
llm_return = st.text_area("Retour LLM", st.session_state.llm_output, height=300)
update_output = st.button("💾 Mettre à jour plan final")

if update_output:
    st.session_state.llm_output = llm_return

# --- Historique et export ---
st.subheader("Plan final / Historique")
st.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.text_area("Output final cumulatif", st.session_state.llm_output, height=350)
