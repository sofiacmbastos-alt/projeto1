import streamlit as st
from datetime import date
import json
import os

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFDDEB;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='color:#FFD1DC;'>Sofia's Reminders 🌸</h1>",
    unsafe_allow_html=True
)

st.write("things i need to do/be reminded of")

st.image("https://polipet.fbitsstatic.net/media/hollandpopicon.png?v=202501081421")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Netherlandwarf.jpg/330px-Netherlandwarf.jpg")

tasks = ["remedio 1", "remedio 2", "academia"]

today = str(date.today())

ARQUIVO = "historico.json"

if os.path.exists(ARQUIVO):
    with open(ARQUIVO, "r") as f:
        historico = json.load(f)
else:
    historico = {}

if today not in historico:
    historico[today] = {task: False for task in tasks}

for task in tasks:
    historico[today][task] = st.checkbox(
        task,
        value=historico[today][task]
    )

with open(ARQUIVO, "w") as f:
    json.dump(historico, f)

done = sum(historico[today].values())
total = len(tasks)

st.progress(done / total)
st.write(f"{done}/{total} completed 🌸")

st.subheader("Histórico 🌸")

for dia, tarefas in historico.items():
    st.markdown(f"### 📅 {dia}")

    for tarefa, feito in tarefas.items():
        if feito:
            st.write(f"✅ {tarefa}")
        else:
            st.write(f"⬜ {tarefa}")
