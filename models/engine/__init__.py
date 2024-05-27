#!/usr/bin/python3
"""Package initializer for HBNB API
"""
from os import getenv
from models.base_model import BaseModel

# Define class mappings
classes = {"User": User, "BaseModel": BaseModel,
          "Place": Place, "State": State,
          "City": City, "Amenity": Amenity,
          "Review": Review}

# Configuration  loading from config file or env variables
STORAGE_TYPE = getenv("HBNB_TYPE_STORAGE", "fs")

# Dependency injection
def get_storage():
  if STORAGE_TYPE == "db":
    from models.engine import db_storage
    return db_storage.DBStorage()
  elif STORAGE_TYPE == "fs":
    from models.engine import file_storage
    return file_storage.FileStorage()
  else:
    raise ValueError(f"Unsupported storage type: {STORAGE_TYPE}")

storage = get_storage()

#logic for logging, error handling, etc.
storage.reload()
