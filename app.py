import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Intelligent Manager MVP", layout="wide")

st.title("Intelligent Manager (MVP Dump + 2 Prompts)")
st.write("Interface simple : input continu + prompts automatiques pour LLM")

# --- Initialisation de la session ---
if "elements" not in st.session_state:
    st.session_state.elements = []  # Liste des éléments initiaux
if "actualisations" not in st.session_state:
    st.session_state.actualisations = []  # Liste des ajouts post-envoi
if "prepared_output" not in st.session_state:
    st.session_state.prepared_output = ""  # Texte collé depuis LLM après prompt 1
if "final_output" not in st.session_state:
    st.session_state.final_output = ""  # Texte collé depuis LLM après prompt 2

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

# --- Prompt 1 : Préparation des éléments de travail ---
st.subheader("Prompt 1 : Préparation des éléments de travail")
prompt1 = "# PROMPT — PRÉPARATION DES ÉLÉMENTS DE TRAVAIL\n"
prompt1 += "Contexte : Tu es un assistant d’analyse et de préparation de travail. On t’envoie une liste d’éléments bruts : tâches, missions, idées, to-do… Ton rôle est de clarifier, reformuler, et décortiquer chaque sujet pour en faire une base exploitable de travail.\n\n"
prompt1 += "Objectif : Pour chaque sujet, tu dois produire une fiche de travail concise et opérationnelle, sous la trame suivante :\n---\nN° sujet : [numéro]\nDescription initiale : [copie brute de l’input]\nReformulation : [formule claire, concise]\nSous-actions : [liste séquentielle d’actions]\nDépendances cachées : [éléments implicites, prérequis, ressources]\n---\nContraintes : Ton sec, net, sans émotion. ⚠️ À clarifier si nécessaire.\n\n"
prompt1 += "Maintenant, traite chaque sujet de la liste ci-dessous :\n\n"
for idx, el in enumerate(st.session_state.elements + st.session_state.actualisations, 1):
    prompt1 += f"Sujet {idx} : {el}\n"

st.text_area("Prompt 1 LLM (copypaste pour traitement)", prompt1, height=300)

# --- Zone pour coller output LLM préparation ---
st.subheader("Coller le retour LLM (Prompt 1)")
prepared_input = st.text_area("Retour LLM (préparation)", st.session_state.prepared_output, height=200)
update_prepared = st.button("💾 Mettre à jour préparation")

if update_prepared:
    st.session_state.prepared_output = prepared_input

# --- Prompt 2 : Séquençage et priorisation ---
st.subheader("Prompt 2 : Séquençage et priorisation")
prompt2 = "# PROMPT — ANALYSE, SÉQUENÇAGE ET PRIORISATION\n"
prompt2 += "Contexte : Tu reçois une série de fiches de travail préparées (une par sujet). Ton rôle est de les traiter comme un système d’opérations pour dégager une séquence optimisée.\n\n"
prompt2 += "Objectif : Hiérarchiser, ordonner et optimiser toutes les actions pour qu’un opérateur humain puisse exécuter la séquence sans hésitation.\n\n"
prompt2 += "Fiches à traiter :\n"
prompt2 += st.session_state.prepared_output + "\n\n"
prompt2 += "Produis l'output selon la trame :\n1️⃣ Synthèse opérationnelle\n2️⃣ Séquençage logique\n3️⃣ Optimisation & simplification\n4️⃣ Jalons clés\n5️⃣ Recommandation d’exécution\n\nConstraints : Lisible, copiable, sans préambule.\n"

st.text_area("Prompt 2 LLM (copypaste pour traitement)", prompt2, height=300)

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
