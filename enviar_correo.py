import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()
REMITENTE = os.getenv("EMAIL_REMITENTE")
CLAVE = os.getenv("EMAIL_CLAVE")
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