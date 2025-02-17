import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from io import StringIO
from geopy.geocoders import Nominatim

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
        
        st.pyplot(fig)
        
        st.write("Mapa de calor de volumen de madera por departamento:")
        heatmap_data = df.groupby("DPTO")["VOLUMEN M3"].sum().reset_index()
        heatmap_data = heatmap_data.pivot_table(values="VOLUMEN M3", index="DPTO")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_data, cmap="Blues", annot=True, fmt=".0f", linewidths=0.5, ax=ax)
        ax.set_title("Mapa de calor del volumen de madera por departamento")
        st.pyplot(fig)
        
        st.write("Mapa de los 10 municipios con mayor movilización de madera:")
        
        # Cargar el shapefile de Colombia
        colombia = gpd.read_file("https://naturalearth.s3.amazonaws.com/50m_cultural\
/ne_50m_admin_0_countries.zip")
        
        # Agrupar los datos por municipio y departamento
        top_municipios = df.groupby(["MUNICIPIO", "DPTO"])["VOLUMEN M3"].sum().nlargest(10).reset_index()
        
        # Unir los datos con el shapefile
        colombia['MUNICIPIO'] = colombia['MUNICIPIO'].str.upper()  # Asegurar que los nombres estén en mayúsculas
        top_municipios['MUNICIPIO'] = top_municipios['MUNICIPIO'].str.upper()
        
        merged = colombia.merge(top_municipios, on="MUNICIPIO", how="inner")
        
        # Crear el mapa
        fig, ax = plt.subplots(figsize=(10, 10))
        colombia.plot(ax=ax, color='lightgray')
        merged.plot(ax=ax, column="VOLUMEN M3", legend=True, cmap="OrRd", markersize=50)
        
        for x, y, label in zip(merged.geometry.centroid.x, merged.geometry.centroid.y, merged["MUNICIPIO"]):
            ax.text(x, y, label, fontsize=8, ha='center')
        
        ax.set_title("Top 10 municipios con mayor movilización de madera")
        ax.set_axis_off()
        
        st.pyplot(fig)

if __name__ == "__main__":
    main()
