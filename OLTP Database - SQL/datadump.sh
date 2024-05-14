#!/bin/bash

# MySQL/MariaDB credentials
DB_USER="root"
DB_PASS="MTAwNzUtaGFyc2hy"
DB_NAME="Sales"

# Dump sales_data table to sales_data.sql file
mysqldump -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" sales_data > sales_data.sql

# Check if the dump was successful
if [ $? -eq 0 ]; then
    echo "Data dumped successfully to sales_data.sql"
else
    echo "Error dumping data"
fi
