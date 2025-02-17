import streamlit as st
import pandas as pd
import requests
from io import StringIO

def load_csv_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("No se pudo cargar el archivo desde la URL.")
        return None

def main():
    st.title("Cargar CSV en Streamlit")
    
    option = st.radio("Selecciona la forma de carga:", ["Subir archivo", "Desde URL"])
    
    df = None
    
    if option == "Subir archivo":
        uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
    
    elif option == "Desde URL":
        url = st.text_input("Ingresa la URL del archivo CSV")
        if url:
            df = load_csv_from_url(url)
    
    if df is not None:
        st.write("Vista previa del dataset:")
        st.dataframe(df)

if __name__ == "__main__":
    main()
