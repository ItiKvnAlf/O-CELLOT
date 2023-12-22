from flask import Flask, render_template
import plotly.express as px
import pandas as pd
import os
import psycopg2

app = Flask(__name__)

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
        cursor.execute("""
            SELECT
                p."Categoría",
                CAST(SUM(CAST(f."Precio Total" AS numeric)) AS text) AS Costo_Total,
                f."Anio" AS Año
            FROM
                facturas f
            JOIN
                productos p ON f."Producto" = p."ID"
            GROUP BY
                p."Categoría", f."Anio";
        """)
        rows = cursor.fetchall()

        # Create a DataFrame from the fetched rows
        df = pd.DataFrame(rows, columns=["Categoría", "Costo_Total", "Año"])

        df["Costo_Total"] = pd.to_numeric(df["Costo_Total"])
        df["Año"] = pd.to_numeric(df["Año"])   

        return df
    except psycopg2.Error as e:
        print("Ocurrió un error al conectar a PostgreSQL: ", e)
    finally:
        if conexion:
            conexion.close()
            print("Datos de productos cargados")

def read_income():
    conexion = None

    try:
        conexion = connect_db()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT 
                a.anio,
                a.Ingresos_Totales,
                b.Costo_Total
            FROM 
                (SELECT 
                    b."Anio" AS anio,
                    SUM(CAST(b."Precio Total" AS NUMERIC)) AS Ingresos_Totales
                FROM 
                    boletas b
                GROUP BY 
                    b."Anio") a
            JOIN 
                (SELECT
                    f."Anio" AS anio,
                    SUM(CAST(f."Precio Total" as numeric)) AS Costo_Total
                FROM
                    facturas f
                GROUP BY
                    f."Anio") b
            ON a.anio = b.anio;
        """)
        rows = cursor.fetchall()

        # Create a DataFrame from the fetched rows
        df = pd.DataFrame(rows, columns=["Año", "Ingresos_Totales", "Costo_Total"])

        df["Ingresos_Totales"] = pd.to_numeric(df["Ingresos_Totales"])
        df["Costo_Total"] = pd.to_numeric(df["Costo_Total"])
        df["Año"] = pd.to_numeric(df["Año"])

        # Add a new column "Beneficio_Total"
        df["Beneficio_Total"] = df["Ingresos_Totales"] - df["Costo_Total"]

        return df
    except psycopg2.Error as e:
        print("Ocurrió un error al conectar a PostgreSQL: ", e)
    finally:
        if conexion:
            conexion.close()
            print("Datos de ingresos cargados")

def read_providers_top10():
    conexion = None

    try:
        conexion = connect_db()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                "Proveedor",
                "Gasto_Total",
                "Anio"
            FROM (
                SELECT
                    p."Proveedor",
                    SUM(CAST(f."Precio Total" as numeric)) AS "Gasto_Total",
                    f."Anio",
                    ROW_NUMBER() OVER (PARTITION BY f."Anio" ORDER BY SUM(CAST(f."Precio Total" as numeric)) DESC) AS "ranking"
                FROM
                    facturas f
                JOIN
                    proveedores p ON f."Proveedor" = p."ID"
                GROUP BY
                    p."Proveedor", f."Anio"
            ) AS ranked_data
            WHERE
                "ranking" <= 10
            ORDER BY
                "Anio" DESC, "Gasto_Total" DESC, "ranking";
        """)
        rows = cursor.fetchall()

        # Create a DataFrame from the fetched rows
        df = pd.DataFrame(rows, columns=["Proveedor", "Gasto_Total", "Anio"])

        df["Gasto_Total"] = pd.to_numeric(df["Gasto_Total"])
        df["Anio"] = pd.to_numeric(df["Anio"])   

        return df
    except psycopg2.Error as e:
        print("Ocurrió un error al conectar a PostgreSQL: ", e)
    finally:
        if conexion:
            conexion.close()
            print("Datos de proveedores cargados")

categories = read_products()
income = read_income()
providers_top10 = read_providers_top10()

def generar_costo_anio_productos(categories):
    fig = px.bar(categories, x='Año', y='Costo_Total', color='Categoría', barmode='group')

    # Personalizar el diseño del gráfico
    fig.update_layout(title='Año vs. Costo Total',
                    xaxis_title='Año',
                    yaxis_title='Costo Total',
                    legend_title='Categoría')
    
    fig.update_layout(updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.8,
            y=1.1,
            showactive=True,
            buttons=list([
                dict(label="Rango de 5 años",
                     method="relayout",
                     args=[
                         {"xaxis.range[0]": categories['Año'].max() - 4.5},
                         {"xaxis.range[1]": categories['Año'].max()}
                     ]
                ),
                dict(label="Rango de 3 años",
                     method="relayout",
                     args=[
                         {"xaxis.range[0]": categories['Año'].max() - 2.5},
                         {"xaxis.range[1]": categories['Año'].max()},
                     ]
                )
            ]),
        ),
    ])

    return fig.to_html(full_html=False)

def generar_ingresos(income):
    fig = px.bar(income, x='Año', y='Ingresos_Totales', color='Ingresos_Totales', barmode='group')

    # Personalizar el diseño del gráfico
    fig.update_layout(title='Ingreso total durante los años...',
                    xaxis_title='Año',
                    yaxis_title='Ingresos Totales',
                    legend_title='Año')

    return fig.to_html(full_html=False)

def generar_costos(income):
    fig = px.line(income, x='Año', y='Costo_Total')

    # Personalizar el diseño del gráfico
    fig.update_layout(title='Año vs. Costos Totales',
                    xaxis_title='Año',
                    yaxis_title='Costos Totales',
                    legend_title='Año')

    return fig.to_html(full_html=False)

def generar_proveedor(providers_top10):
    df_counts = providers_top10.groupby("Proveedor").size().reset_index(name="Frecuencia")

    # Ordenar de mayor a menor por frecuencia
    df_counts = df_counts.sort_values(by="Frecuencia", ascending=True)

    # Creamos el gráfico utilizando Plotly Express
    fig = px.bar(df_counts, x="Frecuencia", y="Proveedor",
                orientation='h',
                title="Frecuencia de Proveedores en el Top 10 a lo largo de los años",
                labels={"Frecuencia": "Número de veces en el Top 10", "Proveedor": "Proveedor"},
                height=600, width=800)

    return fig.to_html(full_html=False)

# Rutas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/categorias')
def products():
    grafico_categorias = generar_costo_anio_productos(categories)
    return render_template('categorias.html', grafico_categorias=grafico_categorias)

@app.route('/ingresos')
def inventory():
    grafico_ingresos = generar_ingresos(income)
    return render_template('ingresos.html', grafico_ingresos=grafico_ingresos)

@app.route('/costos')
def benefits():
    grafico_costos = generar_costos(income)
    return render_template('costos.html', grafico_costos=grafico_costos)

@app.route('/proveedores')
def providers():
    grafico_proveedor = generar_proveedor(providers_top10)
    return render_template('proveedores.html', grafico_proveedor=grafico_proveedor)

if __name__ == '__main__':
    app.run(debug=True)