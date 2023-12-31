# O-CELLOT

# Introducción

Este es un proyecto bajo el área de Ingeniería de Datos, el cual incluye un procedimiento ETL para manipular una cierta cantidad de datos, enfocándose en facturas, precios, inventarios y boletas de una pequeña empresa. El principal objetivo de este proyecto es proporcionar una comprensión profunda y aplicada de los procesos inherentes a la ingeniería de datos.

---
# Comenzando (Modificar nombres de los archivos/ficheros)

## Paso 1: Clonando el repositorio

En primer lugar, se debe clonar este repositorio en el sistema, usando el siguiente comando en el cmd (Símbolo del sistema):

```bash
git clone https://github.com/ItiKvnAlf/O-CELLOT.git
```

o también se puede descargar el archivo ZIP en la sección Code.

En la raíz de este repositorio hay un archivo .cpp, debes compilarlo para obtener archivos de datos como Boletas, Facturas, Inventario y Precios, cubriendo los años desde 2005 hasta 2022. Hay que tomar en cuenta que estos archivos son ficticios, y el el proceso de compilación puede tardar un par de horas hasta que finalice.

## Paso 2: Rutas de las carpetas

Para efectos de este proyecto, las nuevas carpetas (Boletas, Facturas, Inventario y Precios) deben estar en la raíz, al mismo nivel que la carpeta O'CELLOT. Por ejemplo, si se tiene la carpeta O'CELLOT en esta ruta:

- C:\Users\nombre_usuario\O-CELLOT (o bien, la ruta por defecto al clonar el repositorio en el sistema)

La carpeta de datos debe estar en la ruta C:\Users\User\ (ej. C:\Users\nombre_usuario\nombre_carpeta)

*Hay que tomar en consideración que se debe colocar el nombre de esta carpeta de datos en el archivo .env. Esto se explicará con más detalle en el Paso 4.*

## Paso 3: Creando una nueva base de datos

Antes de empezar, es necesario crear y configurar una nueva base de datos para guardar los datos procedentes del proceso ETL de este proyecto. Puedes utilizar, por ejemplo, programas como PgAdmin4 o DBeaver. Simplemente se debe crear una nueva base de datos y asignarle un nombre; las tablas se crearán a partir del script de Python (Paso 6).

## Paso 4: Configurando el archivo .env

Para configurar el nombre de la carpeta de datos y la conexión de la base de datos, debe crear un archivo .env en la carpeta O'CELLOT, el archivo debe contener lo siguiente:

```bash
DATA_FOLDER=nombre_carpeta_datos
DATABASE_URL=postgresql://pg_usuario:pg_contraseña@host:5432/nombre_base_datos
```

en donde:

- *nombre_carpeta_datos*: Este es el nombre de la carpeta en donde se encuentran todos los datos.
- *pg_usuario*: Reemplaza esta variable con el nombre de usuario con el que se creo la base de datos.
- *pg_contraseña*: Modifica este valor con la contraseña configurada para acceder a la base de datos.
- *host*: Puedes reemplazar esta variable con la dirección en donde la base de datos esta alojada (en este nivel de producción se utiliza usualmente *localhost*)
- *5432*: Este es el puerto, no es necesario modificar este valor.
- *nombre_base_datos*: Coloca en este campo el nombre asignada a la base de datos.
---
# Modificando los nombres de archivos/ficheros

Para garantizar que la lectura por parte del script ETL se realice de forma ordenada se hizo necesaria la implementación de un código que modifica los nombres de carpetas y archivos específicos, de tal forma que no hay problemas con el orden de lectura (Ej. Los meses, que se leen de manera alfabética)

## Instalación de módulos

Para que la modificación de los archivos se realice correctamente, es necesario instalar el siguiente módulo, el cual es necesario para leer la carpeta en donde están los datos:

### python-dotenv
Python-dotenv lee pares clave-valor de un archivo .env y puede configurarlos como variables de entorno. Para instalarlo debes escribir lo siguiente:

```bash
pip install python-dotenv
```

## Ejecutando el código modify_folders.py

Una vez instalado el módulo para trabajar con el .env, se debe correr el código con el nombre modify_folders.py, asegurandose de tener en la carpeta mencionada en el .env todos los datos necesarios (Boletas, Facturas y Precios), la carpeta de Inventario se deja de lado, debido a la inconsistencia de las cantidades entre varios productos.

Una vez terminada la ejecución, todas las carpetas de los meses deben para a un nombre con este formato: '*año-mes*'.
A su vez, cada archivo dentro de estas carpetas (En Boletas y Facturas) debe tener como nombre lo siguiente: 'boletas*año-mes-dia*' (Boletas) y 'facturas*año-mes-dia*' (Facturas).

**Nota: el código fue creado en un entorno de Windows, por lo que su funcionamiento en otros sistemas operativos no está garantizado. En Mac, por ejemplo, es necesario modificar las líneas de código que tengan este formato: *anio = foldername.split('\\')[-2]* al siguiente *anio = foldername.split('/')[-2]*, reemplazando '\\' por '/'. Además es necesario controlar los archivos ocultos dentro de las carpeta, como .DS_Store**

---

# Script ETL de Python

## Instalando los modulos

Una vez que se obtienen los datos y el archivo .env está completamente configurado, se debe ejecutar el archivo Python 'etl_script.py'. Pero hay que tener en cuenta que se deben instalar los módulos correspondientes, que son:

### pandas
pandas es una biblioteca de código abierto con licencia BSD que proporciona estructuras de datos y herramientas de análisis de datos de alto rendimiento y fáciles de usar para el lenguaje de programación Python. Se puede instalar mediante pip:

```bash
pip install pandas
```

### sqlalchemy
sqlalchemy está diseñado para un acceso eficiente y de alto rendimiento a bases de datos, adaptado a un lenguaje de dominio simple. Este es el método de instalación:

```bash
pip install SQLAlchemy
```

### psycopg2
psycopg es el adaptador de base de datos PostgreSQL más popular para el lenguaje de programación Python. Este es el comando de instalación:

```bash
pip install psycopg2
```

### openpyxl
openpyxl es una librería de Python para leer/escribir archivos Excel 2010 xlsx/xlsm/xltx/xltm.

```bash
pip install openpyxl
```

## Ejecutando el script de pyhton

Una vez que todos los módulos estén instalados correctamente, ejecutar el script; Puede llevar algo de tiempo, pero se deberían ver los resultados en la terminal, incluido el tiempo necesario para completar cada operación, la cantidad total de archivos en cada carpeta y las primeras 5 filas de uno de los DataFrames.

*Tomar en consideración que antes de ejecutar el script es necesario que las tablas de la base de datos estén vacías, de lo contrario los datos se podrían duplicar*