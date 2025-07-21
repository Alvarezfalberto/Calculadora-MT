import streamlit as st

st.markdown('<h1 style="color:#67c1d3;">Calculadora de Líneas de Media Tensión</h1>', unsafe_allow_html=True)

opcion = st.selectbox(
    "Selecciona el tipo de tramo:",
    ["", "Subterráneo", "Aéreo"]
)

if opcion == "Subterráneo":
    import CalculadoraMT
elif opcion == "Aéreo":
    import Calculadora_MTA
else:
    st.info("Por favor selecciona una opción para continuar.")
