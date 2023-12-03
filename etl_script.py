import os
import time
import pandas as pd

data_folder = 'proyectoidatos2023II'
current_folder = os.getcwd()  # Carpeta actual

def extract_vouchers():
    
    init_time = time.time() #Variable para calcular tiempo de ejecución
    
    vouchers_root_folder = os.path.join(current_folder, '..', data_folder , 'Boletas')  # Carpeta de boletas
    vouchers_dataframes = [] # Lista de dataframes de boletas
    
    for foldername, subfolders, filenames in os.walk(vouchers_root_folder): # Recorre la carpeta de boletas por cada carpeta, subcarpeta y archivo
        for filename in filenames:  # Recorre los archivos de cada carpeta
            if filename.endswith('.csv'):   # Si el archivo es un csv
                file_path = os.path.join(foldername, filename)  # Ruta del archivo
                rows = []
                with open(file_path, 'r') as file:
                    next(file)
                    for line in file:
                        line = line.strip()
                        parts = line.split(',')
                        
                        # Los campos intermedios son productos, y se unen nuevamente en un solo campo
                        products = ','.join(parts[1:-1])
                        
                        rows.append([parts[0], products, parts[-1]])
    
                df = pd.DataFrame(rows, columns=['Boleta', 'Productos', 'Precio Total']) # Crear un DataFrame de pandas
    
                vouchers_dataframes.append(df)  # Agrega el dataframe a la lista
    
    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
    
    print('\n-\tTiempo de ejecución carpeta Boletas:', execution_time, 'segundos') # Imprime el tiempo de ejecución
    return vouchers_dataframes

def extract_bills():
    
    init_time = time.time() #Variable para calcular tiempo de ejecución
    
    bills_root_folder = os.path.join(current_folder, '..',data_folder, 'Facturas')  # Carpeta de facturas
    bills_dataframes = [] # Lista de dataframes de facturas
    
    for foldername, subfolders, filenames in os.walk(bills_root_folder): # Recorre la carpeta de facturas por cada carpeta, subcarpeta y archivo
        for filename in filenames:  # Recorre los archivos de cada carpeta
            if filename.endswith('.csv'):   # Si el archivo es un csv
                file_path = os.path.join(foldername, filename)  # Ruta del archivo
                rows = []
                with open(file_path, 'r') as file:
                    next(file)
                    for line in file:
                        line = line.strip()
                        parts = line.split(',')
                        
                        rows.append([parts[0], parts[1], parts[2],parts[3],parts[4]])
    
                df = pd.DataFrame(rows, columns=['Proveedor', 'Producto', 'Cantidad', 'Precio Unitario', 'Precio Total']) # Crear un DataFrame de pandas
    
                bills_dataframes.append(df)  # Agrega el dataframe a la lista
    
    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
    
    print('\n-\tTiempo de ejecución carpeta Facturas:', execution_time, 'segundos') # Imprime el tiempo de ejecución
    return bills_dataframes

def extract_inventory():
    
    init_time = time.time() #Variable para calcular tiempo de ejecución
    
    inventory_root_folder = os.path.join(current_folder, '..',data_folder, 'Inventario')  # Carpeta de inventario
    inventory_dataframes = [] # Lista de dataframes de inventario
    
    for foldername, subfolders, filenames in os.walk(inventory_root_folder): # Recorre la carpeta de inventario por cada carpeta, subcarpeta y archivo
        for filename in filenames:  # Recorre los archivos de cada carpeta
            if filename.endswith('.csv'):   # Si el archivo es un csv
                file_path = os.path.join(foldername, filename)  # Ruta del archivo
                rows = []
                with open(file_path, 'r') as file:
                    next(file)
                    for line in file:
                        line = line.strip()
                        parts = line.split(',')
                        
                        rows.append([parts[0], parts[1]])
    
                df = pd.DataFrame(rows, columns=['Identificador', 'Cantidad']) # Crear un DataFrame de pandas
    
                inventory_dataframes.append(df)  # Agrega el dataframe a la lista
    
    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
    
    print('\n-\tTiempo de ejecución carpeta Inventario:', execution_time, 'segundos') # Imprime el tiempo de ejecución
    return inventory_dataframes

def extract_prices():
    
    init_time = time.time() #Variable para calcular tiempo de ejecución
    
    prices_root_folder = os.path.join(current_folder, '..', data_folder, 'Precios')  # Carpeta de precios
    prices_dataframes = [] # Lista de dataframes de precios
    
    for foldername, subfolders, filenames in os.walk(prices_root_folder): # Recorre la carpeta de precios por cada carpeta, subcarpeta y archivo
        for filename in filenames:  # Recorre los archivos de cada carpeta
            if filename.endswith('.csv'):   # Si el archivo es un csv
                file_path = os.path.join(foldername, filename)  # Ruta del archivo
                rows = []
                with open(file_path, 'r') as file:
                    next(file)
                    for line in file:
                        line = line.strip()
                        parts = line.split(',')
                        
                        rows.append([parts[0], parts[1]])
    
                df = pd.DataFrame(rows, columns=['Identificador', 'Precio']) # Crear un DataFrame de pandas
    
                prices_dataframes.append(df)  # Agrega el dataframe a la lista
    
    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
    
    print('\n-\tTiempo de ejecución carpeta Precio:', execution_time, 'segundos') # Imprime el tiempo de ejecución
    return prices_dataframes

vouchers = extract_vouchers()
bills = extract_bills()
inventory = extract_inventory()
prices = extract_prices()