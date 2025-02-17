import streamlit as st

# Título de la app
st.title("Mi primera app")

# Autor de la app
st.write("Esta app fue elaborada por COLOQUE AQUÍ SU NOMBRE.")

# Solicitar nombre del usuario
nombre_usuario = st.text_input("¿Cómo te llamas?")

# Mostrar mensaje de bienvenida
if nombre_usuario:
    st.write(f"{nombre_usuario}, te doy la bienvenida a mi primera app.")
