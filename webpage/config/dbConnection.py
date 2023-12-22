import pyodbc

def connection():
    try:
        connection = pyodbc.connect(
            'Driver={SQL Server}; + \
            Servername = ejemplo123;+ \
            Database=ejemplo123; + \
            UID=ejemplo123; + \
            PWD=ejemplo123')
        print("Conexion exitosa")
        cursor = connection.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()

        cursor.execute("SELECT * FROM ejemplo123")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Ocurrio un error al conectar a SQL Server: ", e)

    finally:
        connection.close()
        print("Conexion cerrada")
    
    return connection

conexion = connection() 


    