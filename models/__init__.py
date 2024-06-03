#!/usr/bin/python3
"""
This module sets up the storage system for the AirBnB clone.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Determine the storage type based on environment variable
storage_t = os.getenv('HBNB_TYPE_STORAGE', 'file')

# Database connection setup
if storage_t == "db":
    user = os.getenv('HBNB_MYSQL_USER')
    password = os.getenv('HBNB_MYSQL_PWD')
    host = os.getenv('HBNB_MYSQL_HOST')
    database = os.getenv('HBNB_MYSQL_DB')

    engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}')
    Session = scoped_session(sessionmaker(bind=engine))

    def storage():
        """Returns a scoped session."""
        return Session()

    def close():
        """Closes the session."""
        Session.remove()

else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()

    def storage():
        """Returns the file storage instance."""
        return storage

    def close():
        """Closes the storage (no-op for file storage)."""
        pass
