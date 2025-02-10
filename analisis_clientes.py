import streamlit as st
import pandas as pd
import requests
import io

def load_csv_from_url(url: str) -> pd.DataFrame:
    """
    Descarga un archivo CSV desde una URL y lo carga en un DataFrame de Pandas.
    
    Args:
        url (str): URL del archivo CSV.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados desde el CSV.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción si la solicitud falla
        return pd.read_csv(io.StringIO(response.text))
    except requests.RequestException as e:
        st.error(f"Error al descargar el archivo: {e}")
        return pd.DataFrame()

def load_csv_from_file(uploaded_file) -> pd.DataFrame:
    """
    Carga un archivo CSV subido por el usuario en un DataFrame de Pandas.
    
    Args:
        uploaded_file: Archivo subido por el usuario a través de Streamlit.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados desde el CSV.
    """
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return pd.DataFrame()

def main():
    """
    Función principal de la aplicación Streamlit.
    """
    st.title("Carga de Archivos CSV")
    st.write("Selecciona una opción para cargar un archivo CSV.")
    
    # Uso de radio buttons para permitir solo una selección
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
    
    # Muestra el DataFrame si se ha cargado correctamente
    if not data.empty:
        st.write("Vista previa de los datos:")
        st.dataframe(data)

if __name__ == "__main__":
    main()
