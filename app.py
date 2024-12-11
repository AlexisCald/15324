import pandas as pd
import streamlit as st
from datetime import datetime

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

# Seleccionar proveedor
proveedor = st.selectbox("Selecciona un proveedor:", df['Nombre'].tolist())

# Seleccionar equipo de ventas
equipo = st.selectbox("Selecciona el equipo de ventas:", [f"{i:02d}" for i in range(1, 6)])

# Seleccionar tipo de pedido
tipo = st.radio("Selecciona el tipo de pedido:", ["Pedido", "Cotización"])
tipo_clave = "P" if tipo == "Pedido" else "C"

# Generar clave
if st.button("Generar clave"):
    clave_proveedor = df[df['Nombre'] == proveedor]['Clave'].values[0]
    numero_consecutivo = datetime.now().timetuple().tm_yday
    clave_final = f" | {clave_proveedor}{equipo}{numero_consecutivo:03d}{tipo_clave}"
    st.session_state.clave_generada = clave_final
    st.session_state.mensaje_copiar = "Copiar clave"
    st.success(f"Clave generada: {clave_final}")

# Mostrar la clave generada
if st.session_state.clave_generada:
    st.text_area("Clave generada (Copia manual):", 
                 st.session_state.clave_generada, height=2, 
                 key="clave_generada_text", 
                 help="Copia esta clave manualmente")
