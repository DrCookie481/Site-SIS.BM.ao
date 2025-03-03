import streamlit as st

# Definir duas checkboxes para o gênero
col1, col2 = st.columns(2)

with col1:
    genero_masculino = st.checkbox('Masculino')

with col2:
    genero_feminino = st.checkbox('Feminino')

# Verificar se mais de uma opção foi selecionada
if genero_masculino and genero_feminino:
    st.error("Você pode escolher apenas um gênero.")
elif genero_masculino:
    st.write("Gênero selecionado: Masculino")
elif genero_feminino:
    st.write("Gênero selecionado: Feminino")
else:
    st.write("Nenhum gênero selecionado.")
