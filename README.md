# SoftCart Data Platform Documentation

Welcome to the documentation for the data platform architecture of SoftCart, an ecommerce company. This document provides an overview of the tools, technologies, and processes involved in managing data for SoftCart's operations.

## Table of Contents

- [Introduction](#introduction)
- [OLTP Database - MySQL](#oltp-database---mysql)
- [NoSQL Database - MongoDB](#nosql-database---mongodb)
- [Data Warehouse - PostgreSQL](#data-warehouse---postgresql)
- [Business Intelligence Dashboard - IBM Cognos Analytics](#business-intelligence-dashboard---ibm-cognos-analytics)
- [Data Pipelines - Apache Airflow](#data-pipelines---apache-airflow)
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

SoftCart.com aims to create a data warehouse to generate reports on total sales per year per country, total sales per month per category, total sales per quarter per country, and total sales per category per country.

### Tools / Software

- ERD Design Tool of pgAdmin
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

## Data Pipelines - Apache Airflow

### Overview

In this assignment, you will author an Apache Airflow DAG to analyze a web server log file. The pipeline will extract required lines ending with html, extract specific fields (time stamp, size), transform the data (bytes to mb), and load it by appending to an existing file.

### Software Used

- Apache Airflow

### Exercise 1 - Prepare the Lab Environment

Before starting the assignment:

- Start Apache Airflow.
- Download the dataset from the source and place it in the destination directory mentioned below:
  - **Source**: [accesslog.txt](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/ETL/accesslog.txt)
  - **Destination**: `/home/project/airflow/dags/capstone`

### Exercise 2 - Create a DAG

#### Task 1 - Define the DAG arguments

Create a DAG with the specified arguments.

**Screenshot:** [dag_args.jpg]

#### Task 2 - Define the DAG

Create a DAG named `process_web_log` that runs daily.

**Screenshot:** [dag_definition.jpg]

#### Task 3 - Create a task to extract data

Create a task named `extract_data` to extract the `ipaddress` field from the web server log file and save it into a file named `extracted_data.txt`.

**Screenshot:** [extract_data.jpg]

#### Task 4 - Create a task to transform the data in the txt file

Create a task named `transform_data` to filter out occurrences of `ipaddress` "198.46.149.143" from `extracted_data.txt` and save the output to a file named `transformed_data.txt`.

**Screenshot:** [transform_data.jpg]

#### Task 5 - Create a task to load the data

Create a task named `load_data` to archive `transformed_data.txt` into a tar file named `weblog.tar`.

**Screenshot:** [load_data.jpg]

#### Task 6 - Define the task pipeline

Define the task pipeline as per the provided details.

**Screenshot:** [pipeline.jpg]

### Exercise 3 - Getting the DAG operational

Save the DAG you defined into a file named `process_web_log.py`.

#### Task 7 - Submit the DAG

Take a screenshot of the command you used and the output.

**Screenshot:** [submit_dag.jpg]

#### Task 8 - Unpause the DAG

Take a screenshot of the command you used and the output.

**Screenshot:** [unpause_dag.jpg]

#### Task 9 - Monitor the DAG

Take a screenshot of the DAG runs for the Airflow console.

**Screenshot:** [dag_runs.jpg]

End of the assignment.


## Big Data Analytics Platform - Spark
...
