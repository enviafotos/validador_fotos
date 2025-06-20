import csv
import os
from datetime import datetime
RUTA_HISTORIAL = "historial_envios/historial_envios.csv"
def guardar_en_historial(dni, nombre):
   try:
       os.makedirs("historial_envios", exist_ok=True)  # Crea la carpeta si no existe
       archivo_existe = os.path.exists(RUTA_HISTORIAL)
       with open(RUTA_HISTORIAL, mode='a', newline='', encoding='utf-8') as archivo_csv:
           writer = csv.writer(archivo_csv)
           if not archivo_existe:
               writer.writerow(["DNI", "Nombre", "Fecha y Hora"])
           writer.writerow([dni, nombre, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
       print("✔ Historial guardado correctamente.")
   except Exception as e:
       print("❌ Error al guardar en historial:", e)
