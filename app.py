import streamlit as st
import importlib

st.title("Calculadora MT - Selector de tipo de tramo")

# Menú de selección
opcion = st.selectbox(
    "Selecciona el tipo de tramo:",
    ["Tramo aéreo", "Tramo subterráneo"]
)

# Lógica para llamar al script adecuado
if opcion == "Tramo aéreo":
    modulo_nombre = "Calculadora_MTA"
else:
    modulo_nombre = "CalculadoraMT"

try:
    modulo = importlib.import_module(modulo_nombre)
    importlib.reload(modulo)
    modulo.main()  # El script debe tener una función main()
except Exception as e:
    st.error(f"No se pudo cargar el módulo {modulo_nombre}.py\nError: {e}")
    st.info(f"Asegúrate de que el script tenga una función main() definida.")

