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
from datetime import datetime
load_dotenv()
DESTINATARIO = "mifotobcp@bcp.com.pe"
def validar_nombre_archivo(nombre_archivo):
   patron = r"^(\d+)\s*-\s*(.+)\.jpg$"
   coincidencia = re.match(patron, nombre_archivo, re.IGNORECASE)
   if coincidencia:
       return coincidencia.group(1), coincidencia.group(2)
   return None, None
st.set_page_config(page_title="Validador de fotos", layout="centered")
st.title("📸 Validador de fotos")
st.markdown("Sube tu foto para validarla antes de enviarla.")
st.markdown("""
### ✅ Foto válida:
1. **Tamaño:** 340X402 píxeles (ancho x largo)  
2. **Peso y tipo de archivo:** 25 a 30 kb y formato JPG  
3. **Fondo:** La foto debe ser con fondo de color blanco  
4. **Vestimenta:** Business Casual o Casual  
5. **No Selfie**  
6. El nombre del archivo debe tener la siguiente estructura:  
- Si laboras en LIMA: **DNI - Nombre.jpg**
- Si laboras en PROVINCIA: **DNI - Nombre - Agencia.jpg**
""")
archivo = st.file_uploader("Cargar imagen JPG", type=["jpg"], label_visibility="visible")
if archivo:
   imagen_pil = Image.open(archivo)
   imagen_cv2 = cv2.cvtColor(np.array(imagen_pil), cv2.COLOR_RGB2BGR)
   nombre_archivo = archivo.name
   dni, nombre = validar_nombre_archivo(nombre_archivo)
   if not dni or not nombre:
       st.error("❌ El nombre del archivo debe tener el formato: `DNI - Nombre.jpg`")
   else:
       # Validaciones
       rostro_valido, mensaje_rostro = detectar_rostro_y_encuadre(imagen_pil)
       es_frontal = validar_frontalidad(imagen_cv2)
       rostro_visible_resultado = rostro_visible(imagen_cv2)
       if not rostro_valido:
           st.error(f"❌ {mensaje_rostro}")
       elif not es_frontal:
           st.error("❌ El rostro no está frontal (debe mirar de frente a la cámara).")
       elif not rostro_visible_resultado:
           st.error("❌ El rostro no es completamente visible (puede estar cubierto o con obstrucciones).")
       else:
           st.image(imagen_pil, caption="Imagen validada", width=250)
           st.success("✅ Foto validada correctamente")
           if st.button("📨 Enviar foto"):
               try:
                   # Guardar en historial
                   guardar_en_historial(dni, nombre)
                   # Guardar copia local
                   carpeta_destino = "imagenes_enviadas"
                   os.makedirs(carpeta_destino, exist_ok=True)
                   ruta_imagen = os.path.join(carpeta_destino, f"{dni} - {nombre}.jpg")
                   imagen_pil.save(ruta_imagen)
                   # Enviar correo
                   enviar_correo(
                       destinatario=DESTINATARIO,
                       asunto="Foto validada",
                       mensaje=f"Se adjunta la foto validada de {nombre} (DNI: {dni}).",
                       ruta_imagen=ruta_imagen
                   )
                   st.success("✅ Foto enviada exitosamente por correo.")
               except Exception as e:
                   st.error("❌ Error al enviar el correo:")
                   st.code(traceback.format_exc())