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

import streamlit as st
import math

# Datos de cables subterráneos (Al y Cu)
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

# Factores de corrección (tabla Prysmian)
factores_tabla = {
    'Ca': [('15°C', 1.08), ('20°C', 1.04), ('25°C', 1.00),
           ('30°C', 0.94), ('35°C', 0.88), ('40°C', 0.82)],
    'Cd': [('1 cable', 1.00), ('2 cables', 0.80),
           ('3 cables', 0.70), ('4 cables', 0.65)],
    'Ci': [('Conducto ventilado', 1.00), ('Conducto no ventilado', 0.90),
           ('Canaleta', 0.75), ('Empotrado', 0.50)],
    'Cg': [('50 Ω·m', 1.00), ('100 Ω·m', 0.92),
           ('150 Ω·m', 0.85), ('200 Ω·m', 0.80)],
}

# Inicializar resultados
if 'resultados' not in st.session_state:
    st.session_state.resultados = []

st.title("Calculadora de Líneas de Media Tensión")

# Paso 1: Introducir datos y calcular sección mínima
with st.form("form_datos"):
    st.header("Paso 1: Datos del tramo")
    material = st.selectbox("Material conductor", ["Al", "Cu"])
    cos_phi  = st.number_input("Factor de potencia (cos φ)", min_value=0.0, max_value=1.0,
                               value=0.9, step=0.01)
    tipo     = st.selectbox("Sistema", ["trifasico", "monofasico"])
    V_kV     = st.number_input("Tensión [kV]", value=20.0, step=0.1)
    ID_tramo = st.text_input("ID del tramo")
    Pn_MW    = st.number_input("Potencia Pn [MW]", value=1.0, step=0.1)
    L_m      = st.number_input("Longitud [m]", value=1000.0, step=1.0)

    st.subheader("Factores de corrección")

    # Selección por categoría
    temp_opts = [t for t,_ in factores_tabla['Ca']]
    temp_sel = st.selectbox("Temperatura ambiente", temp_opts)
    Ca = next(val for t,val in factores_tabla['Ca'] if t == temp_sel)

    agr_opts = [a for a,_ in factores_tabla['Cd']]
    agr_sel = st.selectbox("Número de cables (agrupamiento)", agr_opts)
    Cd = next(val for a,val in factores_tabla['Cd'] if a == agr_sel)

    ci_opts = [i for i,_ in factores_tabla['Ci']]
    ci_sel = st.selectbox("Tipo de instalación interior", ci_opts)
    Ci = next(val for i,val in factores_tabla['Ci'] if i == ci_sel)

    cg_opts = [g for g,_ in factores_tabla['Cg']]
    cg_sel = st.selectbox("Resistividad del terreno", cg_opts)
    Cg = next(val for g,val in factores_tabla['Cg'] if g == cg_sel)

    calcular_sec = st.form_submit_button("Calcular sección mínima")

if calcular_sec:
    k_total = Ca * Cd * Ci * Cg
    Pn_W    = Pn_MW * 1e6
    In = (Pn_W / (math.sqrt(3) * V_kV * 1000 * cos_phi)
          if tipo == "trifasico"
          else Pn_W / (V_kV * 1000 * cos_phi))

    # Seleccionar tabla de cables
    data_dict = cable_data_sub_Al if material == "Al" else cable_data_sub_Cu

    # Sección mínima recomendada
    rec = next((s for s in sorted(data_dict) if data_dict[s]["Ia"] * k_total >= In), None)
    rec = rec or max(data_dict)

    # Guardar en session_state
    st.session_state.rec       = rec
    st.session_state.data_dict = data_dict
    st.session_state.In        = In
    st.session_state.Pn_W      = Pn_W
    st.session_state.k_total   = k_total

    st.success(f"Sección mínima recomendada: {rec} mm²")

# Paso 2: Selección de sección y cálculo final
if 'rec' in st.session_state:
    with st.form("form_seccion"):
        st.header("Paso 2: Seleccionar sección")
        rec       = st.session_state.rec
        data_dict = st.session_state.data_dict
        opciones  = [s for s in sorted(data_dict) if s >= rec]
        sec       = st.selectbox("Sección (mm²)", opciones, index=0)
        calcular_tramo = st.form_submit_button("Calcular tramo final")

    if calcular_tramo:
        Ia_corr = data_dict[sec]["Ia"] * st.session_state.k_total
        if Ia_corr < st.session_state.In:
            st.error(f"Corriente insuficiente: In={st.session_state.In:.1f} A > Iac={Ia_corr:.1f} A. "
                     "Seleccione sección ≥ recomendada.")
        else:
            sin_phi = math.sqrt(1 - cos_phi**2)
            Kd, Kl = (math.sqrt(3), 3) if tipo == "trifasico" else (2, 2)
            deltaU_pct = (Kd * st.session_state.In *
                          (data_dict[sec]["R"] * cos_phi + data_dict[sec]["X"] * sin_phi) *
                          (L_m / 1000)) / (V_kV * 1000) * 100
            P_perd_W = Kl * st.session_state.In**2 * data_dict[sec]["R"] * (L_m / 1000)
            Ppn_kW   = P_perd_W / 1000
            Pperd_pct= (P_perd_W / st.session_state.Pn_W) * 100

            st.session_state.resultados.append({
                "ID": ID_tramo,
                "Sección (mm²)": sec,
                "In (A)": f"{st.session_state.In:.1f}",
                "Iac (A)": f"{Ia_corr:.1f}",
                "ΔU (%)": f"{deltaU_pct:.3f}",
                "Pérdida (W)": f"{P_perd_W:.0f}",
                "Ppn (kW)": f"{Ppn_kW:.2f}",
                "Pperd (%)": f"{Pperd_pct:.3f}"
            })
            del st.session_state['rec']

# Mostrar resultados
if st.session_state.resultados:
    st.subheader("Resultados por tramo")
    st.table(st.session_state.resultados)






