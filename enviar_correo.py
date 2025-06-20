import smtplib
from email.message import EmailMessage
import os
import streamlit as st
EMAIL_REMITENTE = st.secrets["EMAIL_REMITENTE"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
def enviar_correo(destinatario, asunto, contenido, archivo_adjunto=None):
   try:
       mensaje = EmailMessage()
       mensaje["From"] = EMAIL_REMITENTE
       mensaje["To"] = destinatario
       mensaje["Subject"] = asunto
       mensaje.set_content(contenido)
       if archivo_adjunto:
           with open(archivo_adjunto, "rb") as f:
               datos_adjunto = f.read()
               nombre_archivo = os.path.basename(archivo_adjunto)
               mensaje.add_attachment(datos_adjunto, maintype="application", subtype="octet-stream", filename=nombre_archivo)
       with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
           smtp.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
           smtp.send_message(mensaje)
       return True
   except Exception as e:
       print(f"Error al enviar el correo: {e}")
       return False
