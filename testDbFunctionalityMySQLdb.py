#!/usr/bin/env python3

import MySQLdb

if True:
    try:
        db = MySQLdb.connect(
            host="localhost",
            user="hbnb_dev",
            passwd="hbnb_dev_pwd",
            db="hbnb_dev_db"
        )
        print("Connection successful!")
        db.close()
    except MySQLdb.OperationalError as e:
        print(f"Connection failed: {e}")

