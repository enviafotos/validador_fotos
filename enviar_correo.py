import smtplib
from email.message import EmailMessage
import os
import streamlit as st
REMITENTE = st.secrets["EMAIL_REMITENTE"]
CLAVE = st.secrets["EMAIL_CLAVE"]
def enviar_correo(destinatario, asunto, mensaje, ruta_imagen):
   msg = EmailMessage()
   msg["Subject"] = asunto
   msg["From"] = REMITENTE
   msg["To"] = destinatario
   msg.set_content(mensaje)
   with open(ruta_imagen, "rb") as f:
       contenido = f.read()
       nombre_archivo = os.path.basename(ruta_imagen)
       msg.add_attachment(contenido, maintype="image", subtype="jpeg", filename=nombre_archivo)
   with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
       smtp.login(REMITENTE, CLAVE)
       smtp.send_message(msg)
