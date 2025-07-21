import streamlit as st

st.markdown('<h1 style="color:#67c1d3;">Calculadora de Líneas de Media Tensión</h1>', unsafe_allow_html=True)

opcion = st.selectbox(
    "Selecciona el tipo de tramo:",
    ["", "Subterráneo", "Aéreo"]
)

if opcion == "Subterráneo":
    import calculadora_mt_sub
elif opcion == "Aéreo":
    import calculadora_mt_aereo
else:
    st.info("Por favor selecciona una opción para continuar.")
