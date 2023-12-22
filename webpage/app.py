from flask import Flask, render_template
import plotly.express as px
import pandas as pd
import os
import psycopg2


app = Flask(__name__)

# Datos de ejemplo
ventas_data = [
    {'Fecha': '2023-01-01', 'Producto': 'A', 'Ventas': 100},
    {'Fecha': '2023-01-02', 'Producto': 'B', 'Ventas': 150},
    {'Fecha': '2023-01-03', 'Producto': 'A', 'Ventas': 80},
]

#coneccion base de datos postgresql
def connect_db():
        conexion = psycopg2.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return conexion

def read_products():
    conexion = None
    try:
        conexion = connect_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        rows = cursor.fetchall()
        return rows
    except psycopg2.Error as e:
        print("Ocurrió un error al conectar a PostgreSQL: ", e)
    finally:
        if conexion:
            conexion.close()
            print("Conexión cerrada")

# Función para generar gráfico de barras
def generar_grafico_barras():
    fig = px.bar(ventas_data, x='Fecha', y='Ventas', color='Producto', title='Ventas por Producto')
    return fig.to_html(full_html=False)

# Función para generar otro gráfico de barras
def generar_otro_grafico_barras():
    fig = px.bar(ventas_data, x='Fecha', y='Ventas', color='Producto', barmode='group', title='Otro Gráfico de Barras')
    return fig.to_html(full_html=False)


# Rutas
@app.route('/')
def home():
    grafico1 = generar_grafico_barras()
    grafico2 = generar_otro_grafico_barras()
    return render_template('home.html', grafico1=grafico1, grafico2=grafico2)

# Poder filtrar por categoría y subcategoría (todos los filtros de producto) y su comportamiento versus tiempo -> Tiempo vs. Costo | Tiempo vs. Beneficio (GRÁFICO)

@app.route('/products')
def products():
    products = read_products()
    return render_template('products.html', products=products)

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