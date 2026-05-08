import streamlit as st

st.markdown(
    "<h1 style='color:#FFD1DC;'>Teste ECMI 2 🌸</h1>",
    unsafe_allow_html=True
)

st.write("Tabela")

st.image(
    "https://polipet.fbitsstatic.net/media/hollandpopicon.png?v=202501081421",
    caption="Remote Image"
)

st.video("https://www.youtube.com/watch?v=uUTraxYVf8o")

nome = st.text_input('type your name here')

if nome:
    st.markdown(
        f"<p style='color:#FFD1DC; font-size:20px;'>{nome} is super cuteee 🩷</p>",
        unsafe_allow_html=True
    )

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Netherlandwarf.jpg/330px-Netherlandwarf.jpg"
)

tasks = ["remedio 1", "remedio 2", "academia"]

for task in tasks:
    st.checkbox(task)
