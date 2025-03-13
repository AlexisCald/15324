import pandas as pd
import streamlit as st
from datetime import datetime
import random

# Leer archivo de proveedores
df = pd.read_excel("prov.xlsx", engine='openpyxl')
df.columns = df.columns.str.strip()

# Configurar la aplicación
st.title("Generador de Claves")

# Solicitar clave de acceso
clave_acceso = st.text_input("Introduce la clave de acceso:", type="password")
if clave_acceso != "D4f4275":
    st.error("Clave incorrecta. Intenta de nuevo.")
    st.stop()

# Inicializar variables de sesión
if "clave_generada" not in st.session_state:
    st.session_state.clave_generada = ""
if "mensaje_copiar" not in st.session_state:
    st.session_state.mensaje_copiar = "Copiar clave"

# Opción de Multicotización
multicotizacion = st.checkbox("Multicotización (Seleccionar varios proveedores)")

if multicotizacion:
    # Permitir seleccionar varios proveedores (opcionalmente dejar vacío)
    proveedores = st.multiselect("Selecciona los proveedores:", df['Nombre'].tolist())
else:
    # Seleccionar un solo proveedor obligatorio
    proveedores = [st.selectbox("Selecciona un proveedor:", df['Nombre'].tolist())]

# Seleccionar equipo de ventas
equipo = st.selectbox("Selecciona el equipo de ventas:", [f"{i:02d}" for i in range(1, 6)])

# Seleccionar tipo de pedido
tipo = st.radio("Selecciona el tipo de pedido:", ["Pedido", "Cotización"])
tipo_clave = "P" if tipo == "Pedido" else "C"

# Generar clave
if st.button("Generar clave"):
    claves_generadas = []
    for proveedor in proveedores:
        clave_proveedor = df[df['Nombre'] == proveedor]['Clave'].values[0] if proveedor else "00"  # Si no hay proveedor, usa "00"
        numero_consecutivo = datetime.now().timetuple().tm_yday
        numero_azar = random.randint(1, 1000)
        clave_final = f" | {clave_proveedor}{equipo}{numero_consecutivo:03d}{numero_azar:03d}{tipo_clave}"
        claves_generadas.append(clave_final)

    # Si no hay proveedores seleccionados en multicotización, se genera una clave general
    if multicotizacion and not proveedores:
        numero_consecutivo = datetime.now().timetuple().tm_yday
        numero_azar = random.randint(1, 1000)
        clave_final = f" | 00{equipo}{numero_consecutivo:03d}{numero_azar:03d}{tipo_clave}"
        claves_generadas.append(clave_final)

    # Guardar clave generada en sesión
    st.session_state.clave_generada = clave_final
    st.session_state.mensaje_copiar = "Copiar clave"
    st.success(f"Clave generada: {clave_final}")

# Mostrar la clave generada
if st.session_state.clave_generada:
    st.text_area("Clave generada (Copia manual):", 
                 st.session_state.clave_generada, height=5, 
                 key="clave_generada_text", 
                 help="Copia esta clave manualmente")
