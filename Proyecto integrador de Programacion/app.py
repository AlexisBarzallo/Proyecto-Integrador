import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
# Título
st.title("App para análisis de desplazamiento y precipitación")

# Subir archivo
archivo = st.file_uploader("Sube el archivo CSV", type=["csv"])

# Si hay archivo cargado
if archivo is not None:
    # Leer archivo en DataFrame
    df = pd.read_csv(archivo)

    # Convertir columna 'Fecha' a formato de fecha si existe
    if 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')  # Si hay errores, pone NaT

    # Mostrar mensaje y tabla
    st.success("Archivo cargado correctamente.")
    st.subheader("Vista previa de los datos:")
    st.dataframe(df, height=600)

    # Mostrar columnas detectadas
    st.subheader("Columnas detectadas:")
    st.write(df.columns.tolist())

    graficos_disponibles = df["Graph_ID"].unique()
    grafico_seleccionado = st.selectbox("Selecciona una figura (Graph_ID):", graficos_disponibles)

    # Filtrar el DataFrame por ese Graph_ID
    df_filtrado = df[df["Graph_ID"] == grafico_seleccionado]

    # Mostrar los datos filtrados
    st.subheader(f"Datos para la figura '{grafico_seleccionado}':")
    st.dataframe(df_filtrado)

    # Mostrar la lista de DP_Number únicos (puede haber uno o varios)
    puntos_unicos = df_filtrado["DP_Number"].unique()
    st.write(f"Puntos de desplazamiento disponibles: {puntos_unicos}")

    st.subheader("Gráfico de desplazamiento y precipitación")

    # Crear figura
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Eje primario (izquierdo): desplazamiento
    ax1.plot(df_filtrado["Date"], df_filtrado["Displacement_cm"], color='blue', marker='o', label='Desplazamiento')
    ax1.set_xlabel("Fecha")
    ax1.set_ylabel("Desplazamiento (cm)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Eje secundario (derecho): precipitación
    ax2 = ax1.twinx()
    ax2.plot(df_filtrado["Date"], df_filtrado["Precipitation_mm"], color='skyblue', linestyle='--', marker='s',
             label='Precipitación')
    ax2.set_ylabel("Precipitación (mm)", color='skyblue')
    ax2.tick_params(axis='y', labelcolor='skyblue')

    # Título y leyenda
    plt.title(f"Figura {grafico_seleccionado.upper()} - Desplazamiento y Precipitación")
    fig.autofmt_xdate()
    fig.tight_layout()
    st.pyplot(fig)

        # Filtrar el DataFrame por el Graph_ID seleccionado
    df_filtrado = df[df["Graph_ID"] == grafico_seleccionado].copy()

    # Convertir la columna Date a formato datetime si no lo está
    df_filtrado["Date"] = pd.to_datetime(df_filtrado["Date"], errors="coerce")

    # Eliminar filas donde la fecha no se pudo convertir
    df_filtrado = df_filtrado.dropna(subset=["Date"])

    # Rango de fechas mínimo y máximo
    fecha_min = df_filtrado["Date"].min().date()
    fecha_max = df_filtrado["Date"].max().date()

    # Mostrar el slider de rango de fechas
    st.subheader("Filtrar por rango de fechas:")
    rango_fechas = st.slider(
        "Selecciona el rango de fechas:",
        min_value=fecha_min,
        max_value=fecha_max,
        value=(fecha_min, fecha_max),
        format="YYYY-MM-DD"
    )

    # Aplicar el filtro por fechas
    fecha_inicio = pd.to_datetime(rango_fechas[0])
    fecha_fin = pd.to_datetime(rango_fechas[1])
    df_filtrado = df_filtrado[
        (df_filtrado["Date"] >= fecha_inicio) &
        (df_filtrado["Date"] <= fecha_fin)
        ]

    # Mostrar los datos filtrados si existen
    if not df_filtrado.empty:
        st.subheader(f"📄 Datos para la figura '{grafico_seleccionado}' entre {fecha_inicio.date()} y {fecha_fin.date()}:")
        st.dataframe(df_filtrado)
    else:
        st.warning("⚠️ No hay datos en el rango de fechas seleccionado.")

else:
    st.info("Por favor, sube un archivo CSV para comenzar.")

