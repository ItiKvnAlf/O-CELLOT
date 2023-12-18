import os
import time
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine


load_dotenv() # Cargar variables de entorno

current_folder = os.getcwd()  # Carpeta actual

def extract_prices():
    
    init_time = time.time() #Variable para calcular tiempo de ejecución
    
    prices_root_folder = os.path.join(current_folder, '..', os.getenv('DATA_FOLDER') , 'Precios')  # Carpeta de precios
    prices_dataframes = [] # Lista de dataframes de precios
    
    for foldername, subfolders, filenames in os.walk(prices_root_folder): # Recorre la carpeta de precios por cada carpeta y archivo
        year = foldername.split('/')[-2]
        month = foldername.split('/')[-1]
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
    
    init_time = time.time()
     
    vouchers_root_folder = os.path.join(current_folder, '..', os.getenv('DATA_FOLDER'), 'Boletas')
    vouchers_dataframes = []
    
    for foldername, subfolders, filenames in os.walk(vouchers_root_folder):
        for filename in filenames:
            if filename != '.DS_Store' and filename.endswith('.csv'):  # Check for file extension
                file_path = os.path.join(foldername, filename)
                
                # Parse file name to get anio, mes, and dia
                anio = filename.split('-')[-1].split('.')[0]
                mes = filename.split('-')[-2]
                dia = ''.join(filter(str.isdigit, filename.split('-')[0]))
                
                rows = []
                with open(file_path, 'r') as file:
                    next(file)
                    for line in file:
                        line = line.strip()
                        parts = line.split(',')
                        products = parts[1:-1]
                        rows.append([parts[0], products, parts[-1], anio, mes, dia])
                if products != []:
                        rows.append([parts[0], products, parts[-1], anio, mes, dia])
                df = pd.DataFrame(rows, columns=['Boleta', 'Productos', 'Precio Total', 'Anio', 'Mes', 'Dia'])
                vouchers_dataframes.append(df)
    
    execution_time = round(time.time() - init_time, 3)
    
    print('\n-\tTiempo de ejecución carpeta Boletas:', execution_time, 'segundos')
    return vouchers_dataframes

def extract_bills():
    
    init_time = time.time()
    
    bills_root_folder = os.path.join(current_folder, '..', os.getenv('DATA_FOLDER'), 'Facturas')
    bills_dataframes = []
    
    for foldername, subfolders, filenames in os.walk(bills_root_folder):
        for filename in filenames:
            if filename != '.DS_Store' and filename.endswith('.csv'):
                file_path = os.path.join(foldername, filename)
                anio = filename.split('-')[-1].split('.')[0]
                mes = filename.split('-')[-2]
                dia = ''.join(filter(str.isdigit, filename.split('-')[0]))
                
                rows = []
                with open(file_path, 'r') as file:
                    next(file)
                    for line in file:
                        line = line.strip()
                        parts = line.split(',')
                        
                        rows.append([parts[0], parts[1], parts[2], parts[3], parts[4], anio, mes, dia])
    
                df = pd.DataFrame(rows, columns=['Proveedor', 'Producto', 'Cantidad', 'Precio Unitario', 'Precio Total', 'Anio', 'Mes', 'Dia'])
                bills_dataframes.append(df)
    
    execution_time = round(time.time() - init_time, 3)
    
    print('\n-\tTiempo de ejecución carpeta Facturas:', execution_time, 'segundos')
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

def transform_to_inventory(vouchers: list, bills: list, products: list):

    init_time = time.time() #Variable para calcular tiempo de ejecución

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
    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
    
    print('\n-\tTiempo de ejecución carpeta Facturas:', execution_time, 'segundos') # Imprime el tiempo de ejecución
    print('-\tCantidad de productos no encontrados:', len(product_not_found)) # Imprime la cantidad de productos no encontrados
    print('-\tCantidad de archivos Inventario:', len(inventory)) #Imprime la cantidad de inventario
    # print('\n',inventory[0].head())
    return inventory

def dataframe_to_sql(dataframe: list, table_name: str, engine: Engine):
    init_time = time.time() #Variable para calcular tiempo de ejecución
    for i, df in enumerate(dataframe): # Recorre la lista de dataframes de precios
        df.to_sql(table_name, con=engine, if_exists='append', index=False) # Inserta los datos del dataframe en la tabla
    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución

    print('\n-\tSe han insertado los datos de', table_name, 'en la base de datos')
    print('-\tTiempo de ejecución:', execution_time, 'segundos') # Imprime el tiempo de ejecución

print('\nIniciando script de ETL')
print('-----------------------')
print('\nLeyendo archivos de datos...')
products = read_products()

prices = extract_prices()
vouchers = extract_vouchers()
bills = extract_bills()

print('\nTransformando datos...')
inventory = transform_to_inventory(vouchers, bills, products)

print('\nInsertando datos en la base de datos POSTGRESQL...')
engine = create_engine(os.getenv('DATABASE_URL')) # DATABASE_URL es una variable de entorno que contiene la cadena de conexión a la base de datos

dataframe_to_sql(prices, 'precios', engine)
dataframe_to_sql(vouchers, 'boletas', engine)
dataframe_to_sql(bills, 'facturas', engine)
dataframe_to_sql(inventory, 'inventario', engine)

engine.dispose() # Cerrar conexión a la base de datos
print('\nSe ha cerrado la conexión a la base de datos')