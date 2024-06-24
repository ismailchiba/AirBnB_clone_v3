#!/bin/bash

# Prompt for the MySQL root password
echo "Please enter the MySQL root password:"
read -s rootpasswd

# Change the root user's password
echo "ALTER USER 'root'@'localhost' IDENTIFIED BY 'khalif01';" | sudo mysql -uroot -p"$rootpasswd"

# Import setup_mysql_test.sql
cat setup_mysql_test.sql | sudo mysql -uroot -p"$rootpasswd"

# Import 100-dump.sql
cat 100-dump.sql | sudo mysql -uroot -p"$rootpasswd"



echo "Operations completed."
