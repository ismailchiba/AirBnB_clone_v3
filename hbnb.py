import os
from sqlalchemy import create_engine
from models.base_model import Base

def init_db():
    env = os.environ.get('HBNB_ENV', 'dev')
    mysql_user = os.environ.get('HBNB_MYSQL_USER')
    mysql_pwd = os.environ.get('HBNB_MYSQL_PWD')
    mysql_host = os.environ.get('HBNB_MYSQL_HOST')
    mysql_db = os.environ.get('HBNB_MYSQL_DB')
    storage_type = os.environ.get('HBNB_TYPE_STORAGE', 'file')

    if storage_type == 'db':
        engine = create_engine('mysql+mysqlconnector://' + mysql_user + ':' + mysql_pwd + '@' + mysql_host + '/' + mysql_db)
        Base.metadata.create_all(engine)
        print("Database initialized successfully")
    else:
        print("Using file storage. No need to initialize a database.")

if __name__ == "__main__":
    init_db()

