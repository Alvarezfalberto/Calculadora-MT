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

# Datos de cables
cable_data_sub_Al = {...}  # (usar el mismo diccionario que antes)
cable_data_sub_Cu = {...}
overhead_data_Al    = {...}
overhead_data_Cu    = {...}

# Estado de resultados
if 'resultados' not in st.session_state:
    st.session_state.resultados = []

st.title("Calculadora de Líneas de Media Tensión")

# Paso 1: Formulario de inputs
with st.form("datos_tramo"):
    st.header("Paso 1: Introduce datos del tramo")
    instal    = st.selectbox("Instalación", ["subterraneo", "aereo"])
    material  = st.selectbox("Material",    ["Al", "Cu"])
    cos_phi   = st.number_input("cos φ", min_value=0.0, max_value=1.0, value=0.9, step=0.01)
    tipo      = st.selectbox("Sistema", ["trifasico", "monofasico"])
    V_kV      = st.number_input("Tensión (kV)", value=20.0, step=0.1)
    ID_tramo  = st.text_input("ID Tramo")
    Pn_MW     = st.number_input("Potencia Pn (MW)", value=1.0, step=0.1)
    L_m       = st.number_input("Longitud (m)",     value=1000.0, step=1.0)

    st.subheader("Factores de corrección")
    Ca = st.number_input("Ca (Temp ambiente)", value=1.0, step=0.01)
    Cd = st.number_input("Cd (Agrupamiento)",  value=1.0, step=0.01)
    Ci = st.number_input("Ci (Instal. interior)", value=1.0, step=0.01)
    Cg = st.number_input("Cg (Suelo)", value=1.0, step=0.01)

    calcular_sec = st.form_submit_button("Calcular sección mínima")

if calcular_sec:
    # Ajuste Cg para aéreo
    Cg_eff = 1.0 if instal == "aereo" else Cg
    k_total = Ca * Cd * Ci * Cg_eff
    Pn_W    = Pn_MW * 1e6
    In = (Pn_W / (math.sqrt(3)*V_kV*1000*cos_phi)
          if tipo=="trifasico" 
          else Pn_W / (V_kV*1000*cos_phi))

    # Selección de diccionario
    if instal == "aereo":
        data_dict = overhead_data_Al if material=="Al" else overhead_data_Cu
    else:
        data_dict = cable_data_sub_Al if material=="Al" else cable_data_sub_Cu

    # Sección mínima
    rec = next((s for s in sorted(data_dict) if data_dict[s]["Ia"]*k_total>=In), None)
    rec = rec or max(data_dict)

    # Guardar en session_state
    st.session_state.rec       = rec
    st.session_state.data_dict = data_dict
    st.session_state.In        = In
    st.session_state.Pn_W      = Pn_W
    st.session_state.k_total   = k_total

    st.success(f"Sección mínima recomendada: {rec} mm²")

# Paso 2: Formulario de selección de sección
if 'rec' in st.session_state:
    with st.form("seleccion_seccion"):
        st.header("Paso 2: Selecciona sección")
        rec = st.session_state.rec
        data_dict = st.session_state.data_dict
        options = [s for s in data_dict if s >= rec]
        sec = st.selectbox("Sección (mm²)", options, index=0)
        calcular_tramo = st.form_submit_button("Calcular tramo final")

    if calcular_tramo:
        Ia_corr = data_dict[sec]["Ia"] * st.session_state.k_total
        if Ia_corr < st.session_state.In:
            st.error(f"In={st.session_state.In:.1f}A > Iac={Ia_corr:.1f}A. " +
                     "Elige sección ≥ recomendada.")
        else:
            sinφ = math.sqrt(1 - cos_phi**2)
            Kd, Kl = (math.sqrt(3), 3) if tipo=="trifasico" else (2, 2)
            deltaU_pct = (
                Kd * st.session_state.In *
                (data_dict[sec]["R"]*cos_phi + data_dict[sec]["X"]*sinφ) *
                (L_m/1000)
                ) / (V_kV*1000) * 100
            P_perd_W = Kl * st.session_state.In**2 * data_dict[sec]["R"] * (L_m/1000)
            Ppn_kW   = P_perd_W / 1000
            Pperd_pct= (P_perd_W / st.session_state.Pn_W)*100

            # Guardar resultado
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

# Mostrar resultados si hay tramos
if st.session_state.resultados:
    st.subheader("Resultados por tramo")
    st.table(st.session_state.resultados)





