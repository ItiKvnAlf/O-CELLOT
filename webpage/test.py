import plotly.express as px
import pandas as pd
import os
import psycopg2

DB_USER='postgres'
DB_PASS='geminianoucn2021'
DB_HOST='localhost'
DB_NAME='ETL'
DB_PORT=5432

conn = psycopg2.connect(
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    host=DB_HOST,
    port=DB_PORT
)

categoria_param = 'Bebé'
subcategoria_param = 'Pañales'

# Replace the date parameters with actual values or variables
anio_param = '2022'

# Construct the SQL query with parameter placeholders
sql_query = """
    SELECT
        p."Categoría",
        p."Sub-categoría",
        CAST(SUM(CAST(f."Precio Total" AS numeric)) AS text) AS Costo_Total
    FROM
        facturas f
    JOIN
        productos p ON f."Producto" = p."ID"
    WHERE
        f."Anio" = %s
        AND (
            p."Categoría" = %s OR
            %s IS NULL
        )
        AND (
            p."Sub-categoría" = %s OR
            %s IS NULL
        )
    GROUP BY
        p."Categoría", p."Sub-categoría";
"""

# Execute the query with parameters
with conn.cursor() as cursor:
    cursor.execute(sql_query, (anio_param, categoria_param, categoria_param, subcategoria_param, subcategoria_param))
    result = cursor.fetchall()

# Do something with the result, e.g., print it
print(result)

# Close the database connection
conn.close()