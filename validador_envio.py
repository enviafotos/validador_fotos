import cv2
import numpy as np
def detectar_rostro_y_encuadre(imagen_pil):
   imagen = cv2.cvtColor(np.array(imagen_pil), cv2.COLOR_RGB2BGR)
   alto_imagen = imagen.shape[0]
   gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
   clasificador = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
   rostros = clasificador.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5)
   if len(rostros) == 0:
       return False, "No se detectó ningún rostro en la imagen."
   for (x, y, w, h) in rostros:
       parte_inferior = y + h
       if parte_inferior < alto_imagen * 0.55:
           return False, "La imagen debe mostrar a la persona desde el pecho hacia arriba."
   return True, "Imagen válida"
def validar_frontalidad(imagen_cv2):
   rostros = detectar_rostros(imagen_cv2)
   return len(rostros) > 0
def rostro_visible(imagen_cv2):
   return True  # Puedes agregar lógica futura para detectar obstrucciones (cabello, mascarilla)
def detectar_rostros(imagen_cv2):
   gris = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2GRAY)
   clasificador = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
   return clasificador.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5)