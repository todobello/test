import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
from utils import get_data_from_api, preprocess_data

# Usamos @st.cache_data para almacenar los datos en caché
@st.cache_data
def load_data():
    data = get_data_from_api()
    df = preprocess_data(data)
    return df

# Función para permitir la descarga de datos filtrados
def download_data(df):
    # Convertir el DataFrame a CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    # Botón para descargar el CSV
    st.download_button(
        label="Descargar datos filtrados en CSV",
        data=csv_data,
        file_name="datos_filtrados.csv",
        mime="text/csv",
    )

# Función para permitir la descarga del gráfico como PNG
def download_graph(fig):
    # Guardar el gráfico como archivo PNG
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    # Botón para descargar el gráfico en formato PNG
    st.download_button(
        label="Descargar gráfico como PNG",
        data=img_buffer,
        file_name="grafico.png",
        mime="image/png"
    )

def app():
    # Cargar los datos desde la API y preprocesarlos dentro de la función
    try:
        df = load_data()  # Usamos la función en caché
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return

    st.title("Visualización de Datos")

    # Opción para seleccionar el tipo de gráfico
    tipo_grafico = st.selectbox("Selecciona el tipo de gráfico:", ["Barra", "Dispersión", "Línea", "Histograma", "Pastel"])

    # Selección de Variables: Ejes X e Y
    columnas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    columna_x = st.selectbox("Selecciona la columna para el eje X", columnas_numericas)
    columna_y = st.selectbox("Selecciona la columna para el eje Y (si aplica)", columnas_numericas)

    # Rango Personalizado para Ejes: Ajustar dinámicamente los límites de los ejes X e Y
    if columna_x:
        min_x, max_x = df[columna_x].min(), df[columna_x].max()
        rango_x = st.slider(f"Selecciona el rango para el eje X ({columna_x})", min_x, max_x, (min_x, max_x))

    if columna_y:
        min_y, max_y = df[columna_y].min(), df[columna_y].max()
        rango_y = st.slider(f"Selecciona el rango para el eje Y ({columna_y})", min_y, max_y, (min_y, max_y))

    # Filtrar los datos según el rango seleccionado
    df_filtrado = df[(df[columna_x] >= rango_x[0]) & (df[columna_x] <= rango_x[1])]
    if columna_y:
        df_filtrado = df_filtrado[(df_filtrado[columna_y] >= rango_y[0]) & (df_filtrado[columna_y] <= rango_y[1])]

    st.write("Datos filtrados por el rango seleccionado:")
    st.dataframe(df_filtrado)

    # Gráfico según la selección
    fig, ax = plt.subplots(figsize=(10, 6))

    if tipo_grafico == "Barra":
        # Gráfico de barras con matplotlib
        df_filtrado[columna_x].value_counts().plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
        ax.set_title(f"Gráfico de Barras: {columna_x}")
        ax.set_xlabel(columna_x)
        ax.set_ylabel('Frecuencia')

    elif tipo_grafico == "Dispersión":
        # Gráfico de dispersión con matplotlib
        ax.scatter(df_filtrado[columna_x], df_filtrado[columna_y], color='green')
        ax.set_title(f"Gráfico de Dispersión: {columna_x} vs {columna_y}")
        ax.set_xlabel(columna_x)
        ax.set_ylabel(columna_y)

    elif tipo_grafico == "Línea":
        # Gráfico de línea con matplotlib
        ax.plot(df_filtrado[columna_x], df_filtrado[columna_y], marker='o', color='orange')
        ax.set_title(f"Gráfico de Línea: {columna_x} vs {columna_y}")
        ax.set_xlabel(columna_x)
        ax.set_ylabel(columna_y)

    elif tipo_grafico == "Histograma":
        # Histograma con matplotlib
        ax.hist(df_filtrado[columna_x], bins=30, color='skyblue', edgecolor='black')
        ax.set_title(f"Histograma de {columna_x}")
        ax.set_xlabel(columna_x)
        ax.set_ylabel('Frecuencia')

    elif tipo_grafico == "Pastel":
        # Gráfico de pastel con pandas (aprovechando value_counts)
        df_filtrado[columna_x].value_counts().plot.pie(autopct='%1.1f%%', ax=ax, startangle=90)
        ax.set_title(f"Gráfico de Pastel de {columna_x}")

    # Mostrar el gráfico
    st.pyplot(fig)

    # Proporcionar la opción para descargar el gráfico en formato PNG
    download_graph(fig)
