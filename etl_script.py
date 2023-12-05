import os
import time
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv() # Cargar variables de entorno

current_folder = os.getcwd()  # Carpeta actual

def extract_vouchers():
    
    init_time = time.time() #Variable para calcular tiempo de ejecución
     
    vouchers_root_folder = os.path.join(current_folder, '..', os.getenv('DATA_FOLDER') , 'Boletas')  # Carpeta de boletas
    vouchers_dataframes = [] # Lista de dataframes de boletas
    
    for foldername, subfolders, filenames in os.walk(vouchers_root_folder): # Recorre la carpeta de boletas por cada carpeta y archivo
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
                        products = parts[1:-1]
                        
                        rows.append([parts[0], products, parts[-1]])
    
                df = pd.DataFrame(rows, columns=['Boleta', 'Productos', 'Precio Total']) # Crear un DataFrame de pandas
    
                vouchers_dataframes.append(df)  # Agrega el dataframe a la lista
    
    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
    
    print('\n-\tTiempo de ejecución carpeta Boletas:', execution_time, 'segundos') # Imprime el tiempo de ejecución
    return vouchers_dataframes

def extract_bills():
    
    init_time = time.time() #Variable para calcular tiempo de ejecución
    
    bills_root_folder = os.path.join(current_folder, '..',os.getenv('DATA_FOLDER') , 'Facturas')  # Carpeta de facturas
    bills_dataframes = [] # Lista de dataframes de facturas
    
    for foldername, subfolders, filenames in os.walk(bills_root_folder): # Recorre la carpeta de facturas por cada carpeta y archivo
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
    
    inventory_root_folder = os.path.join(current_folder, '..',os.getenv('DATA_FOLDER') , 'Inventario')  # Carpeta de inventario
    inventory_dataframes = [] # Lista de dataframes de inventario
    
    for foldername, subfolders, filenames in os.walk(inventory_root_folder): # Recorre la carpeta de inventario por cada carpeta y archivo
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
    
    prices_root_folder = os.path.join(current_folder, '..', os.getenv('DATA_FOLDER') , 'Precios')  # Carpeta de precios
    prices_dataframes = [] # Lista de dataframes de precios
    
    for foldername, subfolders, filenames in os.walk(prices_root_folder): # Recorre la carpeta de precios por cada carpeta y archivo
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
print('-\tCantidad de archivos Boletas:', len(vouchers)) #Imprime la cantidad de boletas
print('\n',vouchers[0].head())

bills = extract_bills()
print('-\tCantidad de archivos Facturas:', len(bills))
print('\n',bills[0].head())

inventory = extract_inventory()
print('-\tCantidad de archivos Inventario:', len(inventory))
print('\n',inventory[0].head())

prices = extract_prices()
print('-\tCantidad de archivos Precios:', len(prices))
print('\n',prices[0].head())

engine = create_engine(os.getenv('DATABASE_URL')) # DATABASE_URL es una variable de entorno que contiene la cadena de conexión a la base de datos

for i, df in enumerate(vouchers):
    table_name = 'voucher'  # Puedes ajustar el nombre de la tabla según tus necesidades
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

print('Se han insertado los datos de boletas')

for i, df in enumerate(bills):
    table_name = 'bill'  # Puedes ajustar el nombre de la tabla según tus necesidades
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

print('Se han insertado los datos de facturas')

for i, df in enumerate(inventory):
    table_name = 'inventory'  # Puedes ajustar el nombre de la tabla según tus necesidades
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

print('Se han insertado los datos de inventario')

for i, df in enumerate(prices):
    table_name = 'price'  # Puedes ajustar el nombre de la tabla según tus necesidades
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

print('Se han insertado los datos de precios')

engine.dispose() # Cerrar conexión a la base de datos
print('Se ha cerrado la conexión a la base de datos')