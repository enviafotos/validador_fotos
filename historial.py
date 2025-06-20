import csv
import os
from datetime import datetime
RUTA_HISTORIAL = "historial_envios.csv"
def guardar_en_historial(dni, nombre):
   # Si el archivo no existe, se crea con encabezado
   archivo_existe = os.path.exists(RUTA_HISTORIAL)
   with open(RUTA_HISTORIAL, mode='a', newline='', encoding='utf-8') as archivo_csv:
       writer = csv.writer(archivo_csv)
       if not archivo_existe:
           writer.writerow(["DNI","Nombre","Fecha y Hora"])
       writer.writerow([dni, nombre, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
