import streamlit as st

# Define nombres de las imágenes para cada sección y configuración
def get_image_names(config, seccion):
    return [
        f"{config}_seccion{seccion}_img1.png",
        f"{config}_seccion{seccion}_img2.png"
    ]

st.title("Calculadora MT Aéreo")

configuracion = st.selectbox("Selecciona la configuración del circuito:", ["Simple", "Doble"])
config_key = 'simple_circuito' if configuracion == "Simple" else 'doble_circuito'

# Supón que tienes 6 secciones para cada configuración
seccion = st.selectbox("Selecciona la sección:", [f"Sección {i+1}" for i in range(6)])
seccion_num = int(seccion.split()[-1])

st.subheader(f"{configuracion} circuito - {seccion}")

# Mostrar las dos imágenes correspondientes
img_names = get_image_names(config_key, seccion_num)
cols = st.columns(2)
for i, img_name in enumerate(img_names):
    try:
        cols[i].image(img_name, caption=img_name, use_column_width="always")
    except Exception as e:
        cols[i].warning(f"No se pudo cargar: {img_name}")

# Resto del código de la calculadora...
# Aquí puedes poner el resto del código de cálculos y resultados

st.info("Sube las imágenes al repositorio con los nombres indicados para visualizarlas aquí.")
