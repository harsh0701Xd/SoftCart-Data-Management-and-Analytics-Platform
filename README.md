# SoftCart Data Platform Documentation

Welcome to the documentation for the data platform architecture of SoftCart, an ecommerce company. This document provides an overview of the tools, technologies, and processes involved in managing data for SoftCart's operations.

## Table of Contents

- [Introduction](#introduction)
- [OLTP Database - MySQL](#oltp-database---mysql)
- [NoSQL Database - MongoDB](#nosql-database---mongodb)
- [Production Data Warehouse - DB2 on Cloud](#production-data-warehouse---db2-on-cloud)
- [Staging Data Warehouse - PostgreSQL](#staging-data-warehouse---postgresql)
- [Big Data Platform - Hadoop](#big-data-platform---hadoop)
- [Big Data Analytics Platform - Spark](#big-data-analytics-platform---spark)
- [Business Intelligence Dashboard - IBM Cognos Analytics](#business-intelligence-dashboard---ibm-cognos-analytics)
- [Data Pipelines - Apache Airflow](#data-pipelines---apache-airflow)
- [Data Processes](#data-processes)

---

## Introduction

SoftCart operates in the ecommerce industry, managing catalog data, transactional data, and analytics data through a hybrid architecture comprising on-premises and cloud-based solutions. This document outlines the architecture and technologies used to manage data effectively.

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

## Production Data Warehouse - DB2 on Cloud
...

## Staging Data Warehouse - PostgreSQL
...

## Big Data Platform - Hadoop
...

## Big Data Analytics Platform - Spark
...

## Business Intelligence Dashboard - IBM Cognos Analytics
...

## Data Pipelines - Apache Airflow
...

## Data Processes
...

