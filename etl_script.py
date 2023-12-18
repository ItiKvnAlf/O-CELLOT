import os
import time
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv() # Cargar variables de entorno

current_folder = os.getcwd()  # Carpeta actual

def extract_prices():
    
    init_time = time.time() #Variable para calcular tiempo de ejecución
    
    prices_root_folder = os.path.join(current_folder, '..', os.getenv('DATA_FOLDER') , 'Precios')  # Carpeta de precios
    prices_dataframes = [] # Lista de dataframes de precios
    
    for foldername, subfolders, filenames in os.walk(prices_root_folder): # Recorre la carpeta de precios por cada carpeta y archivo
        year = foldername.split('\\')[-2]
        month = foldername.split('\\')[-1]
        for filename in filenames:  # Recorre los archivos de cada carpeta
            if filename.endswith('.csv'):   # Si el archivo es un csv
                file_path = os.path.join(foldername, filename)  # Ruta del archivo
                rows = []
                with open(file_path, 'r') as file:
                    next(file)
                    for line in file:
                        line = line.strip()
                        parts = line.split(',')
                        
                        rows.append([parts[0], parts[1],year,month.split('-')[1]])
    
                df = pd.DataFrame(rows, columns=['Identificador', 'Precio', 'Año', 'Mes']) # Crear un DataFrame de pandas
    
                prices_dataframes.append(df)  # Agrega el dataframe a la lista
    
    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
    
    print('\n-\tTiempo de ejecución carpeta Precio:', execution_time, 'segundos') # Imprime el tiempo de ejecución
    return prices_dataframes

def extract_vouchers():
    
    init_time = time.time() #Variable para calcular tiempo de ejecución
     
    vouchers_root_folder = os.path.join(current_folder, '..', os.getenv('DATA_FOLDER') , 'Boletas')  # Carpeta de boletas
    vouchers_dataframes = [] # Lista de dataframes de boletas
    
    for foldername, subfolders, filenames in os.walk(vouchers_root_folder): # Recorre la carpeta de boletas por cada carpeta y archivo
        for filename in filenames:  # Recorre los archivos de cada carpeta
            dia = filename.split('-')[-1].split('.')[0]
            mes = filename.split('-')[-2]
            anio = ''.join(filter(str.isdigit, filename.split('-')[0]))
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
                        
                        rows.append([parts[0], products, parts[-1], anio, mes, dia])
    
                df = pd.DataFrame(rows, columns=['Boleta', 'Productos', 'Precio Total', 'Anio', 'Mes', 'Dia']) # Crear un DataFrame de pandas
    
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
            dia = filename.split('-')[-1].split('.')[0]
            mes = filename.split('-')[-2]
            anio = (''.join(filter(str.isdigit, filename.split('-')[0])))
            if filename.endswith('.csv'):   # Si el archivo es un csv
                file_path = os.path.join(foldername, filename)  # Ruta del archivo
                rows = []
                with open(file_path, 'r') as file:
                    next(file)
                    for line in file:
                        line = line.strip()
                        parts = line.split(',')
                        
                        rows.append([parts[0], parts[1], parts[2],parts[3],parts[4],anio,mes,dia])
    
                df = pd.DataFrame(rows, columns=['Proveedor', 'Producto', 'Cantidad', 'Precio Unitario', 'Precio Total', 'Anio', 'Mes', 'Dia']) # Crear un DataFrame de pandas
        
                bills_dataframes.append(df)  # Agrega el dataframe a la lista

    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
    
    print('\n-\tTiempo de ejecución carpeta Facturas:', execution_time, 'segundos') # Imprime el tiempo de ejecución
    return bills_dataframes

def read_products():
    folder = os.path.join(current_folder, '..', os.getenv('DATA_FOLDER') , 'Productos')  # Carpeta de productos
    products = [] # Lista de productos
    for filename in os.listdir(folder):  # Recorre los archivos de la carpeta
        if filename.endswith('.xlsx'):  # Si el archivo es un xlsx
            file_path = os.path.join(folder, filename) # Ruta del archivo
            df = pd.read_excel(file_path) # Leer el archivo
            for i in range(len(df)): # Recorre el archivo
                products.append(df.iloc[i]['ID']) # Agrega el producto a la lista
    return products

def transform_vouchers(vouchers: list, bills: list, products: list):
    products_amount = len(products) # Cantidad de productos
    amounts = [100] * products_amount # Cantidad de productos en el inventario (100 unidades de cada producto)
    inventory = [] # Lista de dataframes de inventario
    product_not_found = [] # Lista de productos no encontrados
    for i in range(len(bills)):
        rows = [] # Lista de filas del dataframe
        bill = bills[i] # Factura
        voucher = vouchers[i] # Boleta
        for j in range(len(bill)): # Recorre la factura
            product = bill.iloc[j]['Producto'] # Producto
            if product not in products:
                if product not in product_not_found:
                        product_not_found.append(product) # Agrega el producto a la lista de productos no encontrados
            else:
                product_id = products.index(product) # ID del producto
                amounts[product_id] += int(bill.iloc[j]['Cantidad']) # Aumenta la cantidad de productos en el inventario
        for k in range(len(voucher)): # Recorre la boleta
            product_list = voucher.iloc[k]['Productos'] # Lista de productos
            for product in product_list: 
                if product not in products:
                    if product not in product_not_found:
                        product_not_found.append(product) # Agrega el producto a la lista de productos no encontrados
                else:
                    product_id = products.index(product) # ID del producto
                    amounts[product_id] -= 1 # Disminuye la cantidad de productos en el inventario
        for l in range(len(products)):
            rows.append([products[l], amounts[l], voucher.iloc[0]['Anio'], voucher.iloc[0]['Mes'], voucher.iloc[0]['Dia']]) # Agrega la fila al dataframe
        df = pd.DataFrame(rows, columns=['Producto','Cantidad','Anio','Mes','Dia']) # Crear un DataFrame de pandas
        inventory.append(df)    # Agrega el dataframe a la lista
    print('\nALERTA | Algunos productos no están registrados:')
    for product in product_not_found:
        print("\n\t-",product) # Imprime los productos no encontrados
    print("\n")
    return inventory

products = read_products()

prices = extract_prices()
print('-\tCantidad de archivos Precios:', len(prices)) #Imprime la cantidad de precios
# print('\n',prices[0].head())

vouchers = extract_vouchers()
print('-\tCantidad de archivos Boletas:', len(vouchers)) #Imprime la cantidad de boletas
# print('\n',vouchers[0].head())

bills = extract_bills()
print('-\tCantidad de archivos Facturas:', len(bills)) #Imprime la cantidad de facturas
# print('\n',bills[0].head())

inventory = transform_vouchers(vouchers, bills, products)
print('-\tCantidad de archivos Inventario:', len(inventory)) #Imprime la cantidad de inventario
# print('\n',inventory[0].head())

engine = create_engine(os.getenv('DATABASE_URL')) # DATABASE_URL es una variable de entorno que contiene la cadena de conexión a la base de datos

for i, df in enumerate(prices): # Recorre la lista de dataframes de precios
    table_name = 'price' # Nombre de la tabla
    df.to_sql(table_name, con=engine, if_exists='append', index=False) # Inserta los datos del dataframe en la tabla

print('\nSe han insertado los datos de precios')

for i, df in enumerate(vouchers): # Recorre la lista de dataframes de boletas
    table_name = 'voucher' # Nombre de la tabla
    df.to_sql(table_name, con=engine, if_exists='append', index=False) # Inserta los datos del dataframe en la tabla

print('\nSe han insertado los datos de boletas')

for i, df in enumerate(bills): # Recorre la lista de dataframes de facturas
    table_name = 'bill' # Nombre de la tabla
    df.to_sql(table_name, con=engine, if_exists='append', index=False) # Inserta los datos del dataframe en la tabla

print('\nSe han insertado los datos de facturas')

for i, df in enumerate(inventory): # Recorre la lista de dataframes de inventario
    table_name = 'inventory' # Nombre de la tabla
    df.to_sql(table_name, con=engine, if_exists='append', index=False) # Inserta los datos del dataframe en la tabla

print('\nSe han insertado los datos de inventario')

engine.dispose() # Cerrar conexión a la base de datos
print('\n\tSe ha cerrado la conexión a la base de datos')