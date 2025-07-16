#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AlbertoAlvarez
#
# Created:     10/07/2025
# Copyright:   (c) AlbertoAlvarez 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
python3 -m pip install streamlit
import streamlit as st
import math

# Bibliotecas de cables: subterráneos y aéreos, aluminio y cobre
cable_data_sub_Al = {
    50: {"Ia": 130, "R": 0.8180, "X": 0.24},
    70: {"Ia": 160, "R": 0.5650, "X": 0.23},
    95: {"Ia": 190, "R": 0.4080, "X": 0.22},
    120:{"Ia": 215, "R": 0.3230, "X": 0.21},
    150:{"Ia": 245, "R": 0.2630, "X": 0.20},
    185:{"Ia": 280, "R": 0.2100, "X": 0.20},
    240:{"Ia": 320, "R": 0.1610, "X": 0.19},
    300:{"Ia": 365, "R": 0.1300, "X": 0.19},
    400:{"Ia": 415, "R": 0.1020, "X": 0.18},
    500:{"Ia": 480, "R": 0.0805, "X": 0.17},
    630:{"Ia": 545, "R": 0.0640, "X": 0.16},
}

cable_data_sub_Cu = {
    50: {"Ia": 225, "R": 0.3870, "X": 0.18},
    70: {"Ia": 260, "R": 0.2760, "X": 0.17},
    95: {"Ia": 305, "R": 0.2010, "X": 0.16},
    120:{"Ia": 345, "R": 0.1590, "X": 0.16},
    150:{"Ia": 395, "R": 0.1260, "X": 0.15},
    185:{"Ia": 445, "R": 0.1020, "X": 0.15},
    240:{"Ia": 510, "R": 0.0772, "X": 0.14},
    300:{"Ia": 575, "R": 0.0601, "X": 0.14},
    400:{"Ia": 665, "R": 0.0450, "X": 0.13},
}

overhead_data_Al = {
    50: {"Ia": 145, "R": 0.50,   "X": 0.35},
    70: {"Ia": 185, "R": 0.31,   "X": 0.35},
    95: {"Ia": 225, "R": 0.243,  "X": 0.35},
    120:{"Ia": 260, "R": 0.190,  "X": 0.35},
    150:{"Ia": 300, "R": 0.152,  "X": 0.35},
    185:{"Ia": 340, "R": 0.120,  "X": 0.35},
    240:{"Ia": 400, "R": 0.0917, "X": 0.35},
    300:{"Ia": 450, "R": 0.0745, "X": 0.35},
    400:{"Ia": 530, "R": 0.0562, "X": 0.35},
}

overhead_data_Cu = {
    50: {"Ia": 260, "R": 0.24,  "X": 0.28},
    70: {"Ia": 325, "R": 0.17,  "X": 0.27},
    95: {"Ia": 380, "R": 0.123, "X": 0.26},
    120:{"Ia": 440, "R": 0.097, "X": 0.26},
    150:{"Ia": 510, "R": 0.077, "X": 0.25},
    185:{"Ia": 585, "R": 0.058, "X": 0.25},
    240:{"Ia": 680, "R": 0.043, "X": 0.24},
    300:{"Ia": 780, "R": 0.034, "X": 0.23},
}

# Inicializar resultados en session_state
if 'resultados' not in st.session_state:
    st.session_state.resultados = []

st.title("Calculadora de Líneas de Media Tensión")

# Sidebar de entrada de datos
with st.sidebar:
    st.header("Datos del tramo")
    cos_phi = st.number_input("cos φ", min_value=0.0, max_value=1.0, value=0.9, step=0.01)
    tipo = st.selectbox("Sistema", ["trifasico", "monofasico"])
    V_kV = st.number_input("Tensión (kV)", value=20.0, step=0.1)
    ID_tramo = st.text_input("ID Tramo")
    L_m = st.number_input("Longitud (m)", value=1000.0, step=1.0)
    Pn_MW = st.number_input("Potencia Pn (MW)", value=1.0, step=0.1)

    st.subheader("Factores de corrección")
    Ca = st.number_input("Ca (Temp ambiente)", value=1.0, step=0.01)
    Cd = st.number_input("Cd (Agrupamiento)", value=1.0, step=0.01)
    Ci = st.number_input("Ci (Instal. interior)", value=1.0, step=0.01)
    Cg = st.number_input("Cg (Suelo)", value=1.0, step=0.01)

    instal = st.selectbox("Instalación", ["subterraneo", "aereo"])
    material = st.selectbox("Material", ["Al", "Cu"])

    st.markdown("---")
    if st.button("Calcular tramo"):
        # Cálculo de In
        k_total = Ca * Cd * Ci * Cg
        Pn_W = Pn_MW * 1e6
        if tipo == "trifasico":
            In = Pn_W / (math.sqrt(3) * V_kV * 1000 * cos_phi)
        else:
            In = Pn_W / (V_kV * 1000 * cos_phi)

        # Selección de biblioteca
        if instal == "aereo":
            data_dict = overhead_data_Al if material == "Al" else overhead_data_Cu
            Cg = 1.0  # forzar Cg=1 para aéreo
        else:
            data_dict = cable_data_sub_Al if material == "Al" else cable_data_sub_Cu

        # Sección recomendada
        rec = next((s for s, d in sorted(data_dict.items()) if d["Ia"] * k_total >= In), None)
        rec = rec or max(data_dict)
        sec = st.selectbox("Sección seleccionada (mm²)", options=list(data_dict.keys()), index=list(data_dict.keys()).index(rec))

        # Cálculos finales
        data = data_dict[sec]
        Iac = data["Ia"] * k_total
        sin_phi = math.sqrt(1 - cos_phi**2)
        Kd, Kl = (math.sqrt(3), 3) if tipo == "trifasico" else (2, 2)
        deltaU_pct = (Kd * In * (data["R"] * cos_phi + data["X"] * sin_phi) * (L_m/1000)) / (V_kV * 1000) * 100
        P_perd_W = Kl * In**2 * data["R"] * (L_m/1000)
        Ppn_kW = P_perd_W / 1000
        Pperd_pct = (P_perd_W / Pn_W) * 100 if Pn_W else 0

        # Añadir resultado
        st.session_state.resultados.append({
            "ID": ID_tramo,
            "Seccion": sec,
            "In (A)": f"{In:.1f}",
            "Iac (A)": f"{Iac:.1f}",
            "ΔU (%)": f"{deltaU_pct:.3f}",
            "Pérdida (W)": f"{P_perd_W:.0f}",
            "Ppn (kW)": f"{Ppn_kW:.2f}",
            "Pperd (%)": f"{Pperd_pct:.3f}"
        })

# Mostrar resultados acumulados
if st.session_state.resultados:
    st.subheader("Resultados por tramo")
    st.table(st.session_state.resultados)

# Mostrar tablas de factores de corrección en un expander
with st.expander("Tablas de Factores de Corrección"):
    st.write("Ca (Temp ambiente):")
    st.write(f"- 15°C → 1.08  | 20°C → 1.04  | 25°C → 1.00  | 30°C → 0.94  | 35°C → 0.88  | 40°C → 0.82")
    st.write("Cd (Agrupamiento):")
    st.write(f"- 1 cable → 1.00  | 2 cables → 0.80  | 3 cables → 0.70  | 4 cables → 0.65")
    st.write("Ci (Instal. interior):")
    st.write(f"- Conducto ventilado → 1.00  | Conducto no ventilado → 0.90  | Canaleta → 0.75  | Empotrado → 0.50")
    st.write("Cg (Suelo):")
    st.write(f"- 50 Ω·m → 1.00  | 100 Ω·m → 0.92  | 150 Ω·m → 0.85  | 200 Ω·m → 0.80")


