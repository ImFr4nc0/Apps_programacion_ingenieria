import streamlit as st
import pandas as pd
import requests
import io

def load_csv_from_url(url: str) -> pd.DataFrame:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_csv(io.StringIO(response.text))
    except requests.RequestException as e:
        st.error(f"Error al descargar el archivo: {e}")
        return pd.DataFrame()

def load_csv_from_file(uploaded_file) -> pd.DataFrame:
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return pd.DataFrame()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    # Llenar valores faltantes
    if "Nombre" in df_clean.columns:
        df_clean["Nombre"].fillna(df_clean["Nombre"].mode()[0], inplace=True)
    if "Género" in df_clean.columns:
        df_clean["Género"].fillna(df_clean["Género"].mode()[0], inplace=True)
    if "Ingreso Anual" in df_clean.columns:
        df_clean["Ingreso Anual"].fillna(df_clean["Ingreso Anual"].mean(), inplace=True)
    if "Frecuencia de Compra" in df_clean.columns:
        df_clean["Frecuencia de Compra"].fillna(df_clean["Frecuencia de Compra"].mean(), inplace=True)
    if "Historial de Compras" in df_clean.columns:
        df_clean["Historial de Compras"].fillna(df_clean["Historial de Compras"].median(), inplace=True)
    if "Latitud" in df_clean.columns and "Longitud" in df_clean.columns:
        df_clean["Latitud"].interpolate(method="linear", inplace=True)
        df_clean["Longitud"].interpolate(method="linear", inplace=True)

    return df_clean

def main():
    st.title("Análisis de Clientes")
    st.write("Hecho por Alejandro Gómez Franco")
    st.write("Selecciona una opción para cargar un archivo CSV.")

    option = st.radio("Elige un método de carga:", ("Cargar desde URL", "Subir archivo desde la computadora"))

    data = pd.DataFrame()

    if option == "Cargar desde URL":
        url = st.text_input("Introduce la URL del archivo CSV:")
        if url:
            data = load_csv_from_url(url)
    elif option == "Subir archivo desde la computadora":
        uploaded_file = st.file_uploader("Sube un archivo CSV desde tu computadora", type=["csv"])
        if uploaded_file:
            data = load_csv_from_file(uploaded_file)

    if not data.empty:
        st.write("### Datos originales:")
        st.dataframe(data)

        # Aplicar limpieza de datos
        cleaned_data = clean_data(data)

        st.write("### Datos después de la limpieza:")
        st.dataframe(cleaned_data)

if __name__ == "__main__":
    main()
