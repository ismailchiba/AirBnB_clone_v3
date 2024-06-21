#!/usr/bin/python3
import requests

r = requests.get('http://0.0.0.0:5000/1-hbnb/')
print(r.status_code)
