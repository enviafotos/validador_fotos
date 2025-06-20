import csv
import os
from datetime import datetime
def guardar_en_historial(dni, nombre):
   ruta = "historial_envios/historial_envios.csv"
   os.makedirs("historial_envios", exist_ok=True)
   existe = os.path.exists(ruta)
   with open(ruta, mode='a', newline='', encoding='utf-8') as archivo:
       escritor = csv.writer(archivo)
       if not existe:
           escritor.writerow(["DNI", "Nombre", "Fecha y Hora"])
       escritor.writerow([dni, nombre, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
