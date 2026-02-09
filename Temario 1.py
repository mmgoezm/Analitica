import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. Configuración de conexión a tu Google Drive
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Competencia_Ingenieria").sheet1

st.title("🚀 Competencia de Ingeniería en Tiempo Real")

# 2. Formulario de participación
with st.form("quiz_form"):
    nombre = st.text_input("Tu Nombre/Nickname")
    pregunta_1 = st.radio("¿Qué sensor detecta proximidad sin contacto?", ["Capacitivo", "LVDT", "Termocupla"])
    
    submitted = st.form_submit_button("Enviar Respuesta")
    
    if submitted:
        # Lógica de puntos
        puntos = 10 if pregunta_1 == "Capacitivo" else 0
        # Guardar en Google Sheets (Tu Drive)
        sheet.append_row([nombre, puntos])
        st.success("¡Respuesta enviada!")

# 3. Leaderboard en tiempo real
st.subheader("🏆 Tabla de Posiciones")
data = pd.DataFrame(sheet.get_all_records())
if not data.empty:
    leaderboard = data.groupby("nombre")["puntos"].sum().sort_values(ascending=False)
    st.bar_chart(leaderboard)
