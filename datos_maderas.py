import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from io import StringIO

def load_csv_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("No se pudo cargar el archivo desde la URL.")
        return None

def main():
    st.title("Datos madera")
    
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
        st.dataframe(df.head())
        
        st.write("Agrupación por DPTO de especies con sus volúmenes:")
        grouped_df = df.groupby(["DPTO", "ESPECIE"])["VOLUMEN M3"].sum().reset_index()
        sorted_df = grouped_df.sort_values(by=["DPTO", "VOLUMEN M3"], ascending=[True, False])
        st.dataframe(sorted_df)
        
        st.write("Top 10 especies con mayor volumen de madera:")
        top_species = df.groupby("ESPECIE")["VOLUMEN M3"].sum().nlargest(10).reset_index()
        
        fig, ax = plt.subplots()
        ax.barh(top_species["ESPECIE"], top_species["VOLUMEN M3"], color='skyblue')
        ax.set_xlabel("Volumen M3")
        ax.set_ylabel("Especie")
        ax.set_title("Top 10 especies con mayor volumen de madera movilizado")
        ax.invert_yaxis()
        
        st.plt(fig)

if __name__ == "__main__":
    main()
