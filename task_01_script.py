#!/usr/bin/python3
"""
Contains the task one tests
"""
pycodestyle console.py
pycodestyle models/engine/
pycodestyle tests/
HBNB_ENV =test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db HBNB_TYPE_STORAGE=db python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1
