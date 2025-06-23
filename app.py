import os
import re
import cv2
import traceback
import numpy as np
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from enviar_correo import enviar_correo
from validador_envio import detectar_rostro_y_encuadre, validar_frontalidad, rostro_visible
from historial import guardar_en_historial
load_dotenv()
DESTINATARIO = "mifotobcp@bcp.com.pe"
def validar_nombre_archivo(nombre_archivo):
   patron = r"^(\d+)\s*-\s*(.+)\.jpg$"
   coincidencia = re.match(patron, nombre_archivo, re.IGNORECASE)
   if coincidencia:
       return coincidencia.group(1), coincidencia.group(2)
   return None, None
st.title("📸 Validador de Foto para tu Fotocheck")
st.markdown("""
### ✅ Foto válida:
1. **Tamaño:** 340X402 píxeles (ancho x largo)  
2. **Peso y tipo de archivo:** 25 a 30 kb y formato JPG  
3. **Fondo:** La foto debe ser con fondo de color blanco  
4. **Vestimenta:** Business Casual o Casual  
5. **No Selfie**  
6. El nombre del archivo debe tener la siguiente estructura: 
Si laboras en LIMA **DNI - Nombre.jpg**
Si laboras en PROVINCIA **DNI - Nombre - Agencia.jpg**
""")
archivo = st.file_uploader("Sube tu foto", type=["jpg", "jpeg"])
if archivo:
   nombre_archivo = archivo.name
   dni, nombre = validar_nombre_archivo(nombre_archivo)
   if not dni or not nombre:
       st.error("❌ El nombre del archivo debe tener el formato 'DNI - Nombre.jpg'")
   else:
       imagen = Image.open(archivo).convert("RGB")
       imagen_cv2 = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)
       es_valida, mensaje_encuadre = detectar_rostro_y_encuadre(imagen)
       if not es_valida:
           st.error("❌ " + mensaje_encuadre)
       else:
           deteccion = {
               "imagen": imagen_cv2,
               "rostros": cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                         .detectMultiScale(cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5)
           }
           if not validar_frontalidad(deteccion):
               st.error("❌ El rostro no está completamente de frente. Vuelve a tomar la foto.")
           elif not rostro_visible(imagen_cv2, deteccion):
               st.error("❌ El rostro está parcialmente cubierto u obstruido.")
           else:
               st.image(imagen, caption="✅ Foto validada correctamente", width=300)
               if st.button("📤 Enviar foto"):
                   try:
                       ruta_temporal = f"{dni} - {nombre}.jpg"
                       imagen.save(ruta_temporal)
                       enviar_correo(
                           destinatario=DESTINATARIO,
                           asunto="Foto validada correctamente",
                           contenido=f"Se ha validado y enviado la foto de {nombre}.",
                           archivo_adjunto=ruta_temporal
                       )
                       guardar_en_historial(dni, nombre)
                       st.success("✅ Foto enviada correctamente al correo. ¡Gracias!")
                   except Exception as e:
                       detalle_error = traceback.format_exc()
                       st.error("❌ Error al enviar el correo:")
                       st.code(detalle_error, language='python')
                   finally:
                       if os.path.exists(ruta_temporal):
                           os.remove(ruta_temporal)
