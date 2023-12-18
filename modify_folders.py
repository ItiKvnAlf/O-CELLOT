import os
import time
from dotenv import load_dotenv

load_dotenv() # Cargar variables de entorno

current_folder = os.getcwd()  # Carpeta actual

init_time = time.time() #Variable para calcular tiempo de ejecución

def rename_files(root_folder, type):

    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    for foldername, subfolders, filenames in os.walk(root_folder): # Recorre la carpeta de boletas por cada carpeta y archivo
        for filename in filenames:
            anio = filename.split('-')[-1].split('.')[0]
            mes = filename.split('-')[-2]
            dia = (''.join(filter(str.isdigit, filename.split('-')[0]))).zfill(2)

            # Modificar nombres de archivos dentro de meses
            if mes.lower() in meses: # Si el nombre del mes está en la lista de meses
                mes = str(meses.index(mes.lower()) + 1).zfill(2) # Se cambia el nombre del mes a un valor numérico
            
            if filename.endswith('.csv'):  # Si el archivo es un csv
                # Generar el nuevo nombre del archivo
                new_filename = f'{type}{anio}-{mes}-{dia}.csv'

                file_path = os.path.join(foldername, filename)  # Ruta del archivo
                new_file_path = os.path.join(foldername, new_filename)  # Ruta del nuevo archivo

                os.rename(file_path, new_file_path)  # Renombrar el archivo

def rename_folders(root_folder):

    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
             'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

    for foldername, subfolders, filenames in os.walk(root_folder): # Recorre la carpeta de boletas por cada carpeta y archivo
        if foldername.split('\\')[-1].lower() in meses:
                anio = foldername.split('\\')[-2]
                mes = foldername.split('\\')[-1]

                if mes.lower() in meses:
                    mes = str(meses.index(mes.lower()) + 1).zfill(2)
                
                # Renombrar la carpeta a su número correspondiente
                new_foldername = f'{anio}-{mes}'
                folder_path = os.path.join(root_folder, anio)
                new_folder_path = os.path.join(folder_path, new_foldername)
                os.rename(foldername, new_folder_path)

    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución

rename_files(os.path.join(current_folder, '..', os.getenv('DATA_FOLDER'), "Boletas"), "boletas") # Renombrar archivos en Boletas
rename_files(os.path.join(current_folder, '..', os.getenv('DATA_FOLDER'), "Facturas"), "facturas") # Renombrar archivos en Facturas

rename_folders(os.path.join(current_folder, '..', os.getenv('DATA_FOLDER'), "Boletas")) # Renombrar carpetas en Boletas
rename_folders(os.path.join(current_folder, '..', os.getenv('DATA_FOLDER'), "Facturas")) # Renombrar carpetas en Facturas
rename_folders(os.path.join(current_folder, '..', os.getenv('DATA_FOLDER'), "Precios")) # Renombrar carpetas en Precios

execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
print('\n-\tTiempo de ejecución:', execution_time, 'segundos') # Imprime el tiempo de ejecución

