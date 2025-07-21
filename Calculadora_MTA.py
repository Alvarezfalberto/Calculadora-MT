import streamlit as st
import os

# Diccionarios para asociar los textos a claves de archivo
config_map = {
    "Simple circuito a 30 kV": "simple_30kv",
    "Doble circuito a 30 kV": "doble_30kv"
}

seccion_map = {
    "LA-280 dx": "la280_dx",
    "LA-280 sx": "la280_sx",
    "LA-380 sx": "la380_sx",
    "LA-380 dx": "la380_dx",
    "LA-455 sx": "la455_sx",
    "LA-455 dx": "la455_dx"
}

st.title("Calculadora MT Aéreo")

# Selección de configuración
config_text = st.selectbox(
    "Selecciona la configuración del circuito:",
    list(config_map.keys())
)
config_key = config_map[config_text]

# Selección de sección
seccion_text = st.selectbox(
    "Selecciona la sección:",
    list(seccion_map.keys())
)
seccion_key = seccion_map[seccion_text]

# Ruta de la imagen
img_path = os.path.join(".devcontainer", f"{config_key}_{seccion_key}.png")

# Mostrar la imagen correspondiente
try:
    st.image(img_path, caption=f"{config_text} - {seccion_text}", use_container_width="always")
except Exception as e:
    st.warning(f"No se pudo cargar la imagen: {img_path}")


