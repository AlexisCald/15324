import pandas as pd
import streamlit as st
import pyperclip  # Para copiar al portapapeles

# Leer el archivo de proveedores
df = pd.read_excel("prov.xls", engine='xlrd')
df.columns = df.columns.str.strip()

# Configurar la aplicación
st.title("Generador de Claves")

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

# Número consecutivo
if "numero_consecutivo" not in st.session_state:
    st.session_state.numero_consecutivo = 1

# Generar clave
if st.button("Generar clave"):
    clave_proveedor = df[df['Nombre'] == proveedor]['Clave'].values[0]
    clave_final = f" | {clave_proveedor}{equipo}{st.session_state.numero_consecutivo}{tipo_clave}"
    st.session_state.clave_generada = clave_final
    st.session_state.numero_consecutivo += 1
    st.session_state.mensaje_copiar = "Copiar clave"
    st.success(f"Clave generada: {clave_final}")

# Mostrar la clave generada
if st.session_state.clave_generada:
    st.write(f"Clave generada: {st.session_state.clave_generada}")

# Copiar clave
if st.button(st.session_state.mensaje_copiar):
    # Copiar al portapapeles
    pyperclip.copy(st.session_state.clave_generada)
    st.session_state.mensaje_copiar = "Clave copiada!"
    st.success("¡Clave copiada al portapapeles!")
