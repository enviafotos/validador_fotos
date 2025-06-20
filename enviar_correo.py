import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()
EMAIL_REMITENTE = "enviafotos37@gmail.com"
EMAIL_PASSWORD = os.getenv("nsrv kgwk gufh jkoo")  # contraseña de aplicación
def enviar_correo(destinatario, asunto, cuerpo, archivo_adjunto):
   msg = EmailMessage()
   msg['From'] = EMAIL_REMITENTE
   msg['To'] = destinatario
   msg['Subject'] = asunto
   msg.set_content(cuerpo)
   with open(archivo_adjunto, 'rb') as f:
       file_data = f.read()
       file_name = os.path.basename(archivo_adjunto)
       msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)
   with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
       smtp.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
       smtp.send_message(msg)
