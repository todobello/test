import streamlit as st
from utils import get_data_from_api, preprocess_data
import introduccion
import interaccion
import visualizaciones

# Cargar los datos desde la API y preprocesarlos
try:
    data = get_data_from_api()
    df = preprocess_data(data)
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")

# Página de Interacción con los Datos
page = st.sidebar.radio("Selecciona la página", ["App", "Introducción", "Interacción con los Datos", "Gráficos Interactivos"])

if page == "App":
    st.write("Contenido de la App")
if page == "Introducción":
    introduccion.app()
elif page == "Interacción con los Datos":
    interaccion.app(df)  # Pasamos df como argumento aquí
elif page == "Gráficos Interactivos":
    visualizaciones.app()
