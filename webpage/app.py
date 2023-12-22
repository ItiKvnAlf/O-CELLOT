from flask import Flask, render_template
import plotly.express as px
import pandas as pd
import os
import time


app = Flask(__name__)

# Datos de ejemplo
ventas_data = [
    {'Fecha': '2023-01-01', 'Producto': 'A', 'Ventas': 100},
    {'Fecha': '2023-01-02', 'Producto': 'B', 'Ventas': 150},
    {'Fecha': '2023-01-03', 'Producto': 'A', 'Ventas': 80},
]

# Función para generar gráfico de barras
def generar_grafico_barras():
    fig = px.bar(ventas_data, x='Fecha', y='Ventas', color='Producto', title='Ventas por Producto')
    return fig.to_html(full_html=False)

# Función para generar otro gráfico de barras
def generar_otro_grafico_barras():
    fig = px.bar(ventas_data, x='Fecha', y='Ventas', color='Producto', barmode='group', title='Otro Gráfico de Barras')
    return fig.to_html(full_html=False)

def read_products():
    init_time = time.time() #Variable para calcular tiempo de ejecución
    folder = os.path.join(os.getcwd(), '..', 'F' , 'Productos')  # Carpeta de productos
    products = [] # Lista de productos
    for filename in os.listdir(folder):  # Recorre los archivos de la carpeta
        if filename.endswith('.xlsx'):  # Si el archivo es un xlsx
            file_path = os.path.join(folder, filename) # Ruta del archivo
            df = pd.read_excel(file_path) # Leer el archivo
            for i in range(len(df)): # Recorre el archivo
                products.append(df.iloc[i]['ID']) # Agrega el producto a la lista
    execution_time = round(time.time() - init_time, 3) # Calcular el tiempo de ejecución
    print('\n-\tTiempo de lectura de la carpeta de Productos:', execution_time, 'segundos') # Imprime el tiempo de ejecución
    return products

# Rutas
@app.route('/')
def home():
    grafico1 = generar_grafico_barras()
    grafico2 = generar_otro_grafico_barras()
    return render_template('home.html', grafico1=grafico1, grafico2=grafico2)

@app.route('/products')
def products():

    return render_template('products.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/benefits')
def benefits():
    return render_template('benefits.html')

@app.route('/providers')
def providers():
    return render_template('providers.html')

if __name__ == '__main__':
    app.run(debug=True)