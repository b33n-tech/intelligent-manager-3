import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Intelligent Manager 2-temps", layout="wide")
st.title("Intelligent Manager (2-step LLM workflow)")

# --- Session state ---
for key in ["inputs", "step1_output", "step2_output"]:
    if key not in st.session_state:
        st.session_state[key] = []

# --- Chargement des prompts ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "prompts.json"), "r") as f:
    prompts = json.load(f)

prep_prompt = prompts["preparation"]
seq_prompt = prompts["sequencage"]

# --- Input continu ---
st.subheader("Ajouter de nouveaux éléments ou informations contextuelles")
cols = st.columns([6,1])
new_input = cols[0].text_input("Nouvel input (tâche ou info)", key="new_input")
add_button = cols[1].button("➕ Ajouter")

if add_button and new_input.strip() != "":
    st.session_state.inputs.append(new_input.strip())

# --- Affichage cumulatif ---
st.subheader("Éléments cumulés")
for idx, el in enumerate(st.session_state.inputs, 1):
    st.write(f"{idx}. {el}")

# --- Prompt Step 1 ---
st.subheader(f"Prompt 1 — {prep_prompt['title']}")
inputs_text = "\n".join(st.session_state.inputs)
prompt1_text = f"{prep_prompt['instructions']}\n\nÉléments bruts :\n{inputs_text}\n\nFormat attendu :\n{prep_prompt['output_format']}"
st.text_area("Prompt 1 LLM (copypaste)", prompt1_text, height=350)

# --- Retour LLM Step 1 ---
st.subheader("Coller le retour LLM (Step 1)")
step1_return = st.text_area("Retour LLM Step 1", st.session_state.step1_output, height=250)
update_step1 = st.button("💾 Mettre à jour Step 1")

if update_step1:
    st.session_state.step1_output = step1_return

# --- Prompt Step 2 ---
st.subheader(f"Prompt 2 — {seq_prompt['title']}")
prompt2_text = f"{seq_prompt['instructions']}\n\nFiches Step 1 :\n{st.session_state.step1_output}\n\nFormat attendu :\n{seq_prompt['output_format']}"
st.text_area("Prompt 2 LLM (copypaste)", prompt2_text, height=350)

# --- Retour LLM Step 2 ---
st.subheader("Coller le retour LLM (Step 2)")
step2_return = st.text_area("Retour LLM Step 2", st.session_state.step2_output, height=300)
update_step2 = st.button("💾 Mettre à jour plan final")

if update_step2:
    st.session_state.step2_output = step2_return

# --- Historique et export ---
st.subheader("Plan final / Historique")
st.write(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.text_area("Output final cumulatif", st.session_state.step2_output, height=350)
