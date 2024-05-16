# SoftCart Data Platform Documentation

Welcome to the documentation for the data platform architecture of SoftCart, an ecommerce company. This document provides an overview of the tools, technologies, and processes involved in managing data for SoftCart's operations.

![data_platform_architecture](https://github.com/harsh0701Xd/SoftCart-Data-Management-and-Analytics-Platform/assets/89227170/2c507d6e-bf59-4bad-91dd-254e3efc7a00)

## Table of Contents

- [Introduction](#introduction)
- [OLTP Database - MySQL](#oltp-database---mysql)
- [NoSQL Database - MongoDB](#nosql-database---mongodb)
- [Data Warehouse - PostgreSQL](#data-warehouse---postgresql)
- [Business Intelligence Dashboard - IBM Cognos Analytics](#business-intelligence-dashboard---ibm-cognos-analytics)
- [Data Warehouse Synchronization Automation - Python](#data-warehouse-synchronization-automation---python)
- [ETL Data Pipeline - Apache Airflow](etl-data-pipeline---apache-airflow)
- [Big Data Analytics Platform - Spark](#big-data-analytics-platform---spark)

---

## Introduction

SoftCart operates in the ecommerce industry, managing catalog data, transactional data, and analytics data through a hybrid architecture comprising on-premises and cloud-based solutions. SoftCart's online presence is primarily through its website, which customers access using a variety of devices like laptops, mobiles and tablets.
All the catalog data of the products is stored in the MongoDB NoSQL server.
All the transactional data like inventory and sales are stored in the MySQL database server.
SoftCart's webserver is driven entirely by these two databases.
Data is periodically extracted from these two databases and put into the staging data warehouse running on PostgreSQL.
The production data warehouse is on the cloud instance of IBM DB2 server.
BI teams connect to the IBM DB2 for operational dashboard creation. IBM Cognos Analytics is used to create dashboards.
SoftCart uses Hadoop cluster as its big data platform where all the data is collected for analytics purposes.
Spark is used to analyse the data on the Hadoop cluster.
To move data between OLTP, NoSQL and the data warehouse, ETL pipelines are used and these run on Apache Airflow.

## OLTP Database - MySQL

### Overview

SoftCart utilizes MySQL as its OLTP (Online Transaction Processing) database to store transactional data such as inventory and sales.

### Tools / Software

- MySQL 8.0.22
- phpMyAdmin 5.0.4

### Exercise 1 - Check the system environment

- Before proceeding with this section, ensure that the MySQL server is started.

### Exercise 2 - Design the OLTP Database

- Create a database named `sales`.
- Design a table named `sales_data` based on the provided sample data.
```sql
CREATE TABLE sales_data (
    product_id INT,
    customer_id INT,
    price DECIMAL(10, 2),
    quantity INT,
    timestamp TIMESTAMP
);
```
### Exercise 3 - Load the Data

- Download the file oltpdata.csv from the provided link and import the data into the sales_data table using phpMyAdmin.
  
  ![image](https://github.com/harsh0701Xd/SoftCart-Data-Management-and-Analytics-Platform/assets/89227170/b345ffc2-0909-4caa-a387-9e71cdb0f7a9)

- Write a SQL query to find out the count of records in the sales_data table.
  ```sql
  SELECT COUNT(*) FROM sales_data;
  ```

### Exercise 4 - Set up Admin tasks

- Create an index named ts on the timestamp field of the sales_data table.
  ```sql
  CREATE INDEX ts ON sales_data (timestamp);
  ```
- List all indexes on the sales_data table.
  ```sql
  SHOW INDEXES FROM sales_data;
  ```
- Write a bash script named datadump.sh that exports all rows in the sales_data table to a file named sales_data.sql.
  ```
  chmod +x datadump.sh
  ./datadump.sh
  ```
---
  
## NoSQL Database - MongoDB

### Overview

SoftCart utilizes MongoDB as its NoSQL database to store e-commerce catalog data.

### Tools / Software

- MongoDB Server
- MongoDB Command Line Backup Tools

### Exercise 1 - Check the system environment

- Before proceeding with the assignment, check if you have the `mongoimport` and `mongoexport` installed on the lab, otherwise install them.
- Download the `catalog.json` file from [here](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/nosql/catalog.json).

### Exercise 2 - Working with MongoDB

- Import `catalog.json` into MongoDB server into a database named `catalog` and a collection named `electronics`.
  ```
  mongoimport --db catalog --collection electronics --file catalog.json --username root --password MTQyNDktaGFyc2hy --authenticationDatabase admin
  ```
- Create an index on the field “type”
  ```
  db.electronics.createIndex({ "type": 1 })
  ```
- Write a query to find the count of laptops
  ```
  db.electronics.count({ "type": "laptop"})
  ```
- Write a query to find the number of smartphones with a screen size of 6 inches
  ```
  db.electronics.count({ "type": "smart phone"},{"screen size": "6"})
  ```
- Write a query to find out the average screen size of smartphones
  ```
  db.electronics.aggregate([{$match: { "type": "smart phone" }},{$group: {_id: "$type",average_screen_size: { $avg: "$screen size" }}}])
  ```
- Export the fields `_id`, “type”, “model”, from the `electronics` collection into a file named `electronics.csv`
  ```
  mongoexport --host localhost --port 27017 --authenticationDatabase admin --username root --password MTQyNDktaGFyc2hy --db catalog --collection electronics --fields _id,type,model --out electronics.csv
  ```

---

## Data Warehouse - PostgreSQL

### Overview

SoftCart aims to create a data warehouse to generate reports on total sales per year per country, total sales per month per category, total sales per quarter per country, and total sales per category per country.

### Tools / Software

- ERD Design Tool of pgAdminh
- PostgreSQL Database Server

### Exercise 1 - Design a Data Warehouse

- Create a database named `SoftCart`
- Create the following tables:
   - `DimDate`
   - `DimCategory`
   - `DimCountry`
   - `FactSales`
- Design the schema for all the tables:

  ```sql
  CREATE TABLE public."DimDate"
  (
    dateid integer NOT NULL,
    date date,
    Year integer,
    Quarter integer,
    QuarterName character(50),
    Month integer,
    Monthname character(50),
    Day integer,
    Weekday integer,
    WeekdayName character(50),
    CONSTRAINT "DimDate_pkey" PRIMARY KEY (dateid)
  );

  CREATE TABLE public."DimCategory"
  (
    categoryid integer NOT NULL,
    category character(50),
    CONSTRAINT "DimCategory_pkey" PRIMARY KEY (categoryid)
  );

  CREATE TABLE public."DimCountry"
  (
    countryid integer NOT NULL,
    country character(50),
    CONSTRAINT "DimCountry_pkey" PRIMARY KEY (countryid)
  );

  CREATE TABLE public."FactSales"
  (
    Orderid integer NOT NULL,
    dateid integer,
    countryid integer,
    categoryid integer,
    amount integer,
    CONSTRAINT "FactSales_pkey" PRIMARY KEY (orderid)
  );
  ```
  
### Exercise 2 - Loading data

- Download the data from [here](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/datawarehousing/data/DimDate.csv) and load it into the `DimDate` table.
- Download the data from [here](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/datawarehousing/DimCategory.csv) and load it into the `DimCategory` table.
- Download the data from [here](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/datawarehousing/DimCountry.csv) and load it into the `DimCountry` table.
- Download the data from [here](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/datawarehousing/FactSales.csv) and load it into the `FactSales` table.

### Exercise 3 - Queries for Data Analytics

- Create a grouping sets query
  
  ```sql
  SELECT country, category, SUM(amount) AS totalsales
  FROM public."FactSales" fs
  JOIN public."DimCountry" dc ON fs.countryid = dc.countryid
  JOIN public."DimCategory" dcat ON fs.categoryid = dcat.categoryid
  GROUP BY GROUPING SETS ((country), (category), (country, category));
  ```
  ![image](https://github.com/harsh0701Xd/SoftCart-Data-Management-and-Analytics-Platform/assets/89227170/35beef3a-95c6-46f2-83dc-e8e87a5c0c13)

- Create a rollup query

  ```sql
  SELECT dd."year", dc.country, SUM(amount) AS totalsales
  FROM public."FactSales" fs
  JOIN public."DimDate" dd ON fs.dateid = dd.dateid
  JOIN public."DimCountry" dc ON fs.countryid = dc.countryid
  GROUP BY ROLLUP (dd."year", dc.country);
  ```
  ![image](https://github.com/harsh0701Xd/SoftCart-Data-Management-and-Analytics-Platform/assets/89227170/6ec7d0c6-4258-4f2d-a6cd-0c01f051ff8b)

- Create a cube query

  ```sql
  SELECT dd."year", country, AVG(amount) AS average_sales
  FROM public."FactSales" fs
  JOIN public."DimDate" dd ON fs.dateid = dd.dateid
  JOIN public."DimCountry" dc ON fs.countryid = dc.countryid
  GROUP BY CUBE (dd."year", country);
  ```
  ![image](https://github.com/harsh0701Xd/SoftCart-Data-Management-and-Analytics-Platform/assets/89227170/9fcd4e1b-3c54-4a92-bbc0-17da3516a70c)


- Create an MQT

  ```sql
  CREATE MATERIALIZED VIEW total_sales_per_country AS
  SELECT dc.country, SUM(amount) AS total_sales
  FROM public."FactSales" fs
  JOIN public."DimCountry" dc ON fs.countryid = dc.countryid
  GROUP BY dc.country;
  ```
  ![image](https://github.com/harsh0701Xd/SoftCart-Data-Management-and-Analytics-Platform/assets/89227170/f6ed0f2c-dc7d-42c8-b4aa-cfbe99630da6)

---

## Business Intelligence Dashboard - IBM Cognos Analytics

- [Dataset link](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/analytics/ecommerce.csv)
- [Dashboard link](https://us3.ca.analytics.ibm.com/bi/?perspective=dashboard&pathRef=.my_folders%2FEcommerce%2BDashboard&action=view&mode=dashboard&subView=model0000018f77682bc3_00000002)

![image](https://github.com/harsh0701Xd/SoftCart-Data-Management-and-Analytics-Platform/assets/89227170/7b7c3c78-e36f-4864-aceb-c37fee55fa97)

## Data Warehouse Synchronization Automation - Python

### Overview
 
To automate the synchronization between the staging data warehouse (MySQL) and the production data warehouse (PostgreSQL), a python script `automation.py` is used.

### Tools/Software

- MySQL
- PostgreSQL
- Python
- MySQL Connector Python
- psycopg2 (for PostgreSQL)

### Exercise 1 - Retrieving last rowid from postgreSQL database

```
def get_last_rowid():
    postgres_cursor.execute("SELECT MAX(rowid) FROM sales_data;")
    last_rowid = postgres_cursor.fetchone()[0]
    return last_rowid
```

### Exercise 2 - Retrieving all records later than the last rowid from mysql database

```
def get_latest_records(rowid):
    mysql_cursor.execute("SELECT * FROM sales_data WHERE rowid > %s;", (rowid,))
    new_records = mysql_cursor.fetchall()
    return new_records
```

### Exercise 3 - Inserting all retrieved records into the postgreSQL database

```
def insert_records(records):
    for record in records:
        # Check if the number of columns in the record matches the number of columns in the MySQL table
        if len(record) == 4:
            # If the record has 4 columns, insert default values for price and timestamp
            postgres_cursor.execute("INSERT INTO sales_data (rowid, product_id, customer_id, price, quantity, timestamp) VALUES (%s, %s, %s, 0.0, %s, current_timestamp);", record)
        else:
            # If the record has 5 columns, assume the price and timestamp values are provided and insert as is
            postgres_cursor.execute("INSERT INTO sales_data (rowid, product_id, customer_id, price, quantity, timestamp) VALUES (%s, %s, %s, %s, %s, %s);", record)
    postgres_connection.commit()
```

### Exercise 4 - Running `automation.py` script for database synchronization

```
python automation.py
```

--- 

## ETL Data Pipeline - Apache Airflow

### Overview

This section outlines the process of creating a data pipeline using Apache AirFlow. The pipeline is designed to analyze a web server log file, extract specific lines and fields, transform the data, and load it into a tar file.

### Tools/Software

- Apache AirFlow

### Exercise 1 - Define the DAG arguments

- Define necessary arguments for Directed Acyclic Graph (DAG) in Airflow to orchestrate ETL tasks.

  ```
  default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
  }
  ```
  
### Exercise 2 - Define the DAG

- Establish the DAG structure outlining data pipeline workflow in Airflow.

  ```
  dag = DAG(
    dag_id='process_web_log',
    schedule_interval=timedelta(days=1),
    default_args=default_args,
    description='A DAG to process web server log files daily',
    )
  ```

### Exercise 3 - Create tasks to extract,transform and data

- Create a task named `extract_data` to extract the `ipaddress` field from the web server log file and save it into a designated file named `extracted_data.txt`.

  ```
  def extract_data(input_file, output_file):
    with open(input_file, "r") as infile:
        data = infile.read()
        ip_addresses = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', data)
        with open(output_file, "w") as outfile:
            for ip_address in ip_addresses:
                outfile.write(ip_address + '\n')
  ```

- Create a task named `transform_data` to filter out all occurrences of a specified IP address from the `extracted_data.txt` file and save the transformed output to a new file named `transformed_data.txt`.

  ```
  def transform_data(input_file, output_file):
    with open(input_file, "r") as infile:
        transformed_lines = [line for line in infile if line.strip() != "198.46.149.143\n"]
        with open(output_file, "w") as outfile:
            outfile.writelines(transformed_lines)
  ```
  
- Create a task named `load_data` to archive the transformed data file `transformed_data.txt` into a tar file named `weblog.tar`.

  ```
  def load_data():
    os.system("tar -cvf /home/project/airflow/dags/capstone/weblog.tar /home/project/airflow/dags/capstone/transformed_data.txt")
  ```

### Exercise 4 - Define the task pipeline

- Define the sequential flow of tasks to ensure smooth execution of the ETL process.

  ```
  extract_data_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
  )

  transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
  )

  load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
  )
  ```
  
  ```
  extract_data_task >> transform_data_task >> load_data_task
  ```

### Exercise 5 - Submit DAG

- Submit the configured DAG for execution within Airflow environment.

### Exercise 6 - Unpause DAG

- Activate the DAG to initiate scheduled or triggered execution.

---

## Big Data Analytics Platform - Spark

### Overview
This section presents an example of performing big data analytics using Apache Spark with PySpark in a JupyterLab environment. The analysis includes loading and exploring search term data from the e-commerce platform and utilizing a pretrained sales forecasting model to predict sales for the year 2023.

### Software/Tools
- JupyterLab
- PySpark

### Exercise 1 - Installing PySpark

- Installation of PySpark and findspark libraries for working with Apache Spark.

  ```
   !pip install pyspark
   !pip install findspark
  ```

### Exercise 2 - Creating Spark Session and Context
  
- Initializing Spark context and session for data processing.

  ```
  import findspark
  findspark.init()

  from pyspark import SparkContext, SparkConf
  from pyspark.sql import SparkSession
  ```

### Exercise 3 - Loading and Analyzing Search Terms

- Loading search term data into a Spark DataFrame, exploring data characteristics, and performing basic analysis tasks such as counting search occurrences and identifying the top search terms.

  ```
  # Load search term data into a Spark DataFrame
  src = 'searchterms.csv'
  search_term_dataset = spark.read.csv(src)

  # Displaying number of rows and columns
  row_count = search_term_dataset.count()
  col_count = len(search_term_dataset.columns)
  print(f'Row count for search_term_dataset: {row_count}')
  print(f'Column count for search_term_dataset: {col_count}')

  # Displaying the first 5 rows of the dataset
  search_term_dataset.show(5)

  # Performing analysis tasks
  search_term_dataset.createOrReplaceTempView('searches')

  # Count occurrences of a specific search term
  spark.sql('SELECT COUNT(*) FROM searches WHERE _c3="gaming laptop"').show()

  # Identifying top 5 most frequently used search terms
  spark.sql('SELECT _c3, COUNT(_c3) FROM searches GROUP BY _c3 ORDER BY COUNT(_c3) DESC').show(5)
  ```

### Exercise 4 - Sales Forecasting Model

- Utilizing a pretrained sales forecasting model to predict sales for the year 2023.

  ```
  # Load pretrained sales forecasting model
  from pyspark.ml.regression import LinearRegressionModel
  sales_prediction_model = LinearRegressionModel.load('sales_prediction.model')

  # Predict sales for the year 2023
  from pyspark.ml.feature import VectorAssembler
  def predict(year):
      assembler = VectorAssembler(inputCols=["year"],outputCol="features")
      data = [[year,0]]
      columns = ["year", "sales"]
      _ = spark.createDataFrame(data, columns)
      __ = assembler.transform(_).select('features','sales')
      predictions = sales_prediction_model.transform(__)
      predictions.select('prediction').show()
      # Perform prediction
      predict(2023)
  ```
  
---
