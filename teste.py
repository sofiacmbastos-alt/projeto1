import streamlit as st

st.title('Teste ECMI 2')
st.write("Tabela")

st.image("https://polipet.fbitsstatic.net/media/hollandpopicon.png?v=202501081421", caption="Remote Image")

st.video("https://www.youtube.com/watch?v=uUTraxYVf8o")

nome = st.text_input('type your name here')
if nome:
    st.write(nome, 'is super cuteee *-*')

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Netherlandwarf.jpg/330px-Netherlandwarf.jpg")
