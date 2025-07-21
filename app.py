import streamlit as st
import importlib

st.title("Calculadora MT Aéreo")

# Opciones y mapeos
opciones = {
    "Simple circuito a 30 kV": "simple_30kv",
    "Doble circuito a 30 kV": "doble_30kv"
}

config_text = st.selectbox("Selecciona la configuración del circuito:", list(opciones.keys()))
script_name = opciones[config_text]

secciones = [
    "LA-280 dx", "LA-280 sx", "LA-380 sx",
    "LA-380 dx", "LA-455 sx", "LA-455 dx"
]
seccion_text = st.selectbox("Selecciona la sección:", secciones)

# Mostrar imagen asociada (ajusta la ruta si es necesario)
import os
img_path = os.path.join(".devcontainer", f"{script_name}_{seccion_text.lower().replace(' ', '_').replace('-', '')}.png")
if os.path.exists(img_path):
    st.image(img_path, caption=f"{config_text} - {seccion_text}", use_column_width="always")
else:
    st.warning(f"No se pudo cargar la imagen: {img_path}")

# Dinámicamente importar y ejecutar el script correspondiente
try:
    module = importlib.import_module(script_name)
    importlib.reload(module)
    module.main(seccion_text)  # Asegúrate de que cada script tenga una función main(seccion)
except Exception as e:
    st.warning(f"No se pudo cargar el script {script_name}.py: {e}")

