import os
import time
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv() # Cargar variables de entorno

current_folder = os.getcwd()  # Carpeta actual

def rename_folders_and_files(root_folder):
    init_time = time.time() #Variable para calcular tiempo de ejecución

    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    for foldername, subfolders, filenames in os.walk(root_folder): # Recorre la carpeta de boletas por cada carpeta y archivo
        for filename in filenames:
            anio = filename.split('-')[-1].split('.')[0]
            mes = filename.split('-')[-2]
            dia = (''.join(filter(str.isdigit, filename.split('-')[0]))).zfill(2)

            # Modificar nombres de archivos dentro de meses
            if mes.lower() in meses: # Si el nombre del mes está en la lista de meses
                mes = str(meses.index(mes.lower()) + 1).zfill(2)
            
            if filename.endswith('.csv'):  # Si el archivo es un csv
                # Generar el nuevo nombre del archivo
                new_filename = f'boletas{anio}-{mes}-{dia}.csv'

                file_path = os.path.join(foldername, filename)  # Ruta del archivo
                new_file_path = os.path.join(foldername, new_filename)  # Ruta del nuevo archivo

                os.rename(file_path, new_file_path)  # Renombrar el archivo
    
    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
    
    print('\n-\tTiempo de ejecución:', execution_time, 'segundos') # Imprime el tiempo de ejecución

rename_folders_and_files(os.path.join(current_folder, '..', os.getenv('DATA_FOLDER'), "Boletas")) # Renombrar carpetas y archivos en Boletas