import os
import time
import pandas as pd
from dotenv import load_dotenv
import calendar
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
                        
                        rows.append([parts[0], parts[1],year,month])
    
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
            anio = filename.split('-')[-1].split('.')[0]
            mes = filename.split('-')[-2]
            dia = ''.join(filter(str.isdigit, filename.split('-')[0]))
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
            anio = filename.split('-')[-1].split('.')[0]
            mes = filename.split('-')[-2]
            dia = (''.join(filter(str.isdigit, filename.split('-')[0])))
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
    products = []
    for filename in os.listdir(folder):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(folder, filename)
            df = pd.read_excel(file_path)
            for i in range(len(df)):
                products.append(df.iloc[i]['ID'])
    return products

def transform_vouchers(vouchers: list, bills: list, products: list):
    products_amount = len(products)
    amounts = [100] * products_amount
    inventory = []
    product_not_found = []
    cant = 0
    for i in range(len(bills)):
        rows = []
        bill = bills[i]
        voucher = vouchers[i]
        print(cant)
        for j in range(len(bill)):
            product = bill.iloc[j]['Producto']
            if product not in products:
                if product not in product_not_found:
                        product_not_found.append(product)
            else:
                product_id = products.index(product)
                amounts[product_id] += int(bill.iloc[j]['Cantidad'])
        for k in range(len(voucher)):
            product_list = voucher.iloc[k]['Productos']
            for product in product_list:
                if product not in products:
                    if product not in product_not_found:
                        product_not_found.append(product)
                else:
                    product_id = products.index(product)
                    amounts[product_id] -= 1
        for l in range(len(products)):
            rows.append([products[l], amounts[l], voucher.iloc[i]['Anio'], voucher.iloc[i]['Mes'], voucher.iloc[i]['Dia']])
        df = pd.DataFrame(rows, columns=['Producto','Cantidad','Anio','Mes','Dia'])
        inventory.append(df)
        cant += 1
    print('\nALERTA | Algunos productos no están registrados:')
    for product in product_not_found:
        print("\n\t-",product)
    print("\n")
    return inventory

products = read_products()

prices = extract_prices()
print('-\tCantidad de archivos Precios:', len(prices)) #Imprime la cantidad de precios
print('\n',prices[0].head())

vouchers = extract_vouchers()
print('-\tCantidad de archivos Boletas:', len(vouchers)) #Imprime la cantidad de boletas
print('\n',vouchers[0].head())

bills = extract_bills()
print('-\tCantidad de archivos Facturas:', len(bills)) #Imprime la cantidad de facturas
print('\n',bills[0].head())

inventory = transform_vouchers(vouchers, bills, products)

for i, df in enumerate(inventory):
    print(df)
print('-\tCantidad de archivos Inventario:', len(inventory)) #Imprime la cantidad de inventario

engine = create_engine(os.getenv('DATABASE_URL')) # DATABASE_URL es una variable de entorno que contiene la cadena de conexión a la base de datos

for i, df in enumerate(prices):
    table_name = 'price'
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

print('\nSe han insertado los datos de precios')

for i, df in enumerate(vouchers):
    table_name = 'voucher'
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

print('\nSe han insertado los datos de boletas')

for i, df in enumerate(bills):
    table_name = 'bill'
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

print('\nSe han insertado los datos de facturas')

for i, df in enumerate(inventory):
    table_name = 'inventory'
    df.to_sql(table_name, con=engine, if_exists='append', index=False)

print('\nSe han insertado los datos de inventario')

engine.dispose() # Cerrar conexión a la base de datos
print('\n\tSe ha cerrado la conexión a la base de datos')