# AirBnB Clone V3

## Author
Tadala N. Kapengule

## System Requirements
```python
pip install flask
pip install sqlalchemy
```
Compiled on __Ubuntu 22.04 LTS__ with __Python 3.12__

## Tasks

### 1. Never fail!

The following requirements must be met for your project:

- **all** current tests must pass (don’t delete them…)
- add new tests as much as you can (tests are mandatory for some tasks)

### 2. Improve storage

Update DBStorage and FileStorage, adding two new methods. All changes should be done in the branch storage_get_count:

__A method to retrieve one object__:

- Prototype:
	```python
	def get(self, cls, id):
	""" 	
		cls: class
		id: string representing the object ID
	"""
	```
- Returns the object based on the ``class`` and its ID, or ``None`` if not found

__A method to count the number of objects in storage__:

- Prototype:
	```python
	def count(self, cls=None):
	""" cls: class (optional) """
	```
- Returns the number of objects in storage matching the given ``class``. If no ``class`` is passed, returns the count of all objects in storage.

__File(s)__

``models/engine/db_storage.py``, ``models/engine/file_storage.py``, ``tests/test_models/test_engine/test_db_storage.py``, ``tests/test_models/test_engine/test_file_storage.py``

### 3. Status of your API

It’s time to start your API!

Your first endpoint (route) will be to return the status of your API:

```bash
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app

# Terminal 2

curl -X GET http://0.0.0.0:5000/api/v1/status
```

- Create a folder ``api`` at the root of the project with an empty file ``__init__.py``
- Create a folder ``v1`` inside ``api``:
	- create an empty file __init__.py
	- create a file ``app.py``:
		- create a variable ``app``, instance of ``Flask``
		- import ``storage`` from ``models``
		- import ``app_views`` from ``api.v1.views``
		- register the blueprint ``app_views`` to your Flask instance ``app``
		- declare a method to handle ``@app.teardown_appcontext`` that calls ``storage.close()``
		- inside if ``__name__ == "__main__"``:, run your Flask server (variable ``app``) with:
			- ``host`` = environment variable ``HBNB_API_HOST`` or ``0.0.0.0`` if not defined
			- ``port`` = environment variable ``HBNB_API_PORT`` or ``5000`` if not defined
			- ``threaded``=``True``
- Create a folder ``views`` inside ``v1``:
	- create a file ``__init__.py``:
		- import ``Blueprint`` from flask ``doc``
		- create a variable ``app_views`` which is an instance of Blueprint (url prefix must be ``/api/v1``)
		- wildcard import of everything in the package ``api.v1.views.index`` => ``PEP8`` will complain about it, don’t worry, it’s normal and this file (``v1/views/__init__.py``) won’t be check.
	- create a file ``index.py``
	- import ``app_views`` from ``api.v1.views``
	- create a route /status on the object ``app_views`` that returns a JSON: ``"status": "OK"`` (see example)

__File__

``api/__init__.py``, ``api/v1/__init__.py``, ``api/v1/views/__init__.py``, ``api/v1/views/index.py``, ``api/v1/app.py``

### 4. Some stats?

Create an endpoint that retrieves the ``number`` of each objects by ``type``:

- In ``api/v1/views/index.py``
- Route: ``/api/v1/stats``
- You must use the newly added ``count()`` method from ``storage``

```bash
curl -X GET http://0.0.0.0:5000/api/v1/stats
#RESPONSE
{
  "amenities": 47, 
  "cities": 36, 
  "places": 154, 
  "reviews": 718, 
  "states": 27, 
  "users": 31
}
```

__File__
``api/v1/views/index.py``
