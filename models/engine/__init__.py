#!/usr/bin/python3
"""Models will be int. with a package."""

from os import getenv


giv_stor = getenv("HBNB_TYPE_STORAGE")

if giv_stor == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
