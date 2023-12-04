# O-CELLOT
---

# Introduction

This is a project under the topic of Data Engineering, which includes an ETL procedure to manipulate a certain amount of data, focusing on bills, prices, inventory and vouchers from a small business. The main objective of this proyect is to provide a deep and applied understanding of the processes inherent to data engineering.

---

# Getting started

## Step 1

First up, clone this repository into your system, using the following command in the cmd:

```bash
git clone https://github.com/ItiKvnAlf/O-CELLOT.git
```

or download the ZIP file in the Code section.

In the root of this repository there is a .cpp file, you must compile it to obtain data files such as Vouchers, Bills, Inventory and Prices, covering the years from 2005 up to 2022. Notice that this files are fictional, and the compiling process may take a couple of hours until is finished.

## Step 2

For purposes of this project, the new folders (Vouchers, Bills, Inventory and Prices) must be at the root, at the same level as the O'CELLOT folder. For example, if you have the O'CELLOT folder in this route:

- C:\Users\User\O-CELLOT (or your default route once you clone this repository into your system)
- The Data folder must be in the C:\Users\User\ route (ex. C:\Users\User\folder_name)

*Notice that you must put this data folder name in the .env file. This will be explained in Step 4.*

## Step 3

Before starting, it is necessary to create and configure a new database to save the data in the ETL process of this project. You can use programs like PgAdmin4 or DBeaver, for instance. Just create a new database and give it a name; the tables will be created from the pyhton script.

## Step 4

To configure the name of the data folder and the connection of the database, you must create a .env file in the O'CELLOT folder, the file must contain the following:

```bash
DATA_FOLDER=data_folder_name
DATABASE_URL=postgresql://pg_username:pg_password@host:5432/database
```

in which:

- *data_folder_name*: This is the name of the folder in which all the data is saved.
- *pg_username*: Replace this variable with your database username.
- *pg_password*: Replace with the password set to access the database.
- *host*: You can replace this field with the address in which the database is hosted (at this level of production it may be *localhost*)
- *5432*: This is the port, it is not necessary to modify this value.
- *database*: Put in this field the name of the database

## Step 5

Once the data is obtained and the .env file is fully configurated, you must run python file 'etl_script.py'. But keep in mind that you must install the corresponding modules, which are:

### time
### pandas
pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language. It can be installed via pip:

```bash
pip install pandas
```

### python-dotenv
Python-dotenv reads key-value pairs from a .env file and can set them as environment variables. To install it, you must type the following:

```bash
pip install python-dotenv
```

### sqlalchemy
sqlalchemy provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language. This is the installation method:

```bash
pip install SQLAlchemy
```

## Step 6

Once all the modules are successfully installed, you can run the script; it may take some time, but you should see the results in the terminal, including the time required to complete each operation, the total amount of files in each folder and the first 5 rows of one of the DataFrames.
