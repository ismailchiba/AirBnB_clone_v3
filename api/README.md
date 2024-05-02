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

### 5. Not found

In ``api/v1/app.py``, create a handler for ``404`` errors that returns a JSON-formatted ``404`` status code response. The content should be: ``"error": "Not found"``.

```bash
curl -X GET http://0.0.0.0:5000/api/v1/nop

#RESPONSE
{
  "error": "Not found"
}
curl -X GET http://0.0.0.0:5000/api/v1/nop -vvv
```

__File__

``api/v1/app.py``

### 6. State

Create a new view for ``State`` objects that handles all default RESTFul API actions:

- In the file ``api/v1/views/states.py``
- You must use ``to_dict()`` to retrieve an object into a valid JSON
- Update ``api/v1/views/__init__.py`` to import this new file

Retrieves the list of all ``State`` objects: ``GET /api/v1/states``

Retrieves a ``State`` object: ``GET /api/v1/states/<state_id>``

- If the ``state_id`` is not linked to any ``State`` object, raise a ``404`` error

Deletes a ``State`` object:: ``DELETE /api/v1/states/<state_id>``

- If the ``state_id`` is not linked to any ``State`` object, raise a ``404`` error
- Returns an empty dictionary with the status code ``200``

Creates a ``State``: ``POST /api/v1/states``

- You must use ``request.get_json`` from Flask to transform the HTTP body request to a dictionary
- If the HTTP body request is not valid JSON, raise a ``400`` error with the message ``Not a JSON``
- If the dictionary doesn’t contain the key name, raise a ``400`` error with the message ``Missing name``
- Returns the new ``State`` with the status code ``201``

Updates a ``State`` object: ``PUT /api/v1/states/<state_id>``

- If the ``state_id`` is not linked to any ``State`` object, raise a ``404`` error
- You must use ``request.get_json`` from Flask to transform the HTTP body request to a dictionary
- If the HTTP body request is not valid JSON, raise a ``400`` error with the message ``Not a JSON``
- Update the ``State`` object with all key-value pairs of the dictionary.
- Ignore keys: ``id``, ``created_at`` and ``updated_at``
- Returns the ``State`` object with the status code ``200``

```bash
curl -X GET http://0.0.0.0:5000/api/v1/states/
#RESPONSE
[
  {
    "__class__": "State", 
    "created_at": "2017-04-14T00:00:02", 
    "id": "8f165686-c98d-46d9-87d9-d6059ade2d99", 
    "name": "Louisiana", 
    "updated_at": "2017-04-14T00:00:02"
  }, 
  {
    "__class__": "State", 
    "created_at": "2017-04-14T16:21:42", 
    "id": "1a9c29c7-e39c-4840-b5f9-74310b34f269", 
    "name": "Arizona", 
    "updated_at": "2017-04-14T16:21:42"
  }, 
...
]

curl -X GET http://0.0.0.0:5000/api/v1/states/8f165686-c98d-46d9-87d9-d6059ade2d99
#RESPONSE
{
  "__class__": "State", 
  "created_at": "2017-04-14T00:00:02", 
  "id": "8f165686-c98d-46d9-87d9-d6059ade2d99", 
  "name": "Louisiana", 
  "updated_at": "2017-04-14T00:00:02"
}

curl -X POST http://0.0.0.0:5000/api/v1/states/ -H "Content-Type: application/json" -d '{"name": "California"}' -vvv
#RESPONSE
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> POST /api/v1/states/ HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.51.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 22
> 
* upload completely sent off: 22 out of 22 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 195
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sat, 15 Apr 2017 01:30:27 GMT
< 
{
  "__class__": "State", 
  "created_at": "2017-04-15T01:30:27.557877", 
  "id": "feadaa73-9e4b-4514-905b-8253f36b46f6", 
  "name": "California", 
  "updated_at": "2017-04-15T01:30:27.558081"
}
* Curl_http_done: called premature == 0
* Closing connection 0

curl -X PUT http://0.0.0.0:5000/api/v1/states/feadaa73-9e4b-4514-905b-8253f36b46f6 -H "Content-Type: application/json" -d '{"name": "California is so cool"}'
#RESPONSE
{
  "__class__": "State", 
  "created_at": "2017-04-15T01:30:28", 
  "id": "feadaa73-9e4b-4514-905b-8253f36b46f6", 
  "name": "California is so cool", 
  "updated_at": "2017-04-15T01:51:08.044996"
}

curl -X GET http://0.0.0.0:5000/api/v1/states/feadaa73-9e4b-4514-905b-8253f36b46f6
#RESPONSE
{
  "__class__": "State", 
  "created_at": "2017-04-15T01:30:28", 
  "id": "feadaa73-9e4b-4514-905b-8253f36b46f6", 
  "name": "California is so cool", 
  "updated_at": "2017-04-15T01:51:08"
}

curl -X DELETE http://0.0.0.0:5000/api/v1/states/feadaa73-9e4b-4514-905b-8253f36b46f6
#RESPONSE
{}

curl -X GET http://0.0.0.0:5000/api/v1/states/feadaa73-9e4b-4514-905b-8253f36b46f6
#RESPONSE
{
  "error": "Not found"
}
```

__File__

``api/v1/views/states.py``, ``api/v1/views/__init__.py``

### 7. City

Same as ``State``, create a new view for ``City`` objects that handles all default RESTFul API actions:

- In the file ``api/v1/views/cities.py``
- You must use ``to_dict()`` to serialize an object into valid JSON
- Update ``api/v1/views/__init__.py`` to import this new file

Retrieves the list of all ``City`` objects: ``GET /api/v1/states/<state_id>/cities``

Retrieves a ``City`` object: ``GET /api/v1/cities/<city_id>``

- If the ``city_id`` is not linked to any ``City`` object, raise a ``404`` error

Deletes a ``City`` object:: ``DELETE /api/v1/cities/<city_id>``

- If the ``city_id`` is not linked to any ``City`` object, raise a ``404`` error
- Returns an empty dictionary with the status code ``200``

Creates a ``City``: ``POST /api/v1/states/<state_id>/cities``

- You must use ``request.get_json`` from Flask to transform the HTTP body request to a dictionary
- If the HTTP body request is not valid JSON, raise a ``400`` error with the message ``Not a JSON``
- If the dictionary doesn’t contain the key name, raise a ``400`` error with the message ``Missing name``
- Returns the new ``City`` with the status code ``201``

Updates a ``City`` object: ``PUT /api/v1/cities/<city_id>``

- If the ``city_id`` is not linked to any ``City`` object, raise a ``404`` error
- You must use ``request.get_json`` from Flask to transform the HTTP body request to a dictionary
- If the HTTP body request is not valid JSON, raise a ``400`` error with the message ``Not a JSON``
- Update the ``City`` object with all key-value pairs of the dictionary.
- Ignore keys: ``id``, ``state_id``, ``created_at`` and ``updated_at``
- Returns the ``City`` object with the status code ``200``

__File__
``api/v1/views/cities.py``, ``api/v1/views/__init__.py``

### 8. Amenity

Create a new view for ``Amenity`` objects that handles all default RESTFul API actions:

- In the file ``api/v1/views/amenities.py``
- You must use ``to_dict()`` to retrieve an object into a valid JSON
- Update ``api/v1/views/__init__.py`` to import this new file

Retrieves the list of all ``Amenity`` objects: ``GET /api/v1/amenities``

Retrieves a ``Amenity`` object: ``GET /api/v1/amenities/<amenity_id>``

- If the ``amenity_id`` is not linked to any ``Amenity`` object, raise a ``404`` error

Deletes a ``Amenity`` object:: ``DELETE /api/v1/amenities/<amenity_id>``

- If the ``amenity_id`` is not linked to any ``Amenity`` object, raise a ``404`` error
- Returns an empty dictionary with the status code ``200``

Creates a ``Amenity``: ``POST /api/v1/amenities``

- You must use ``request.get_json`` from Flask to transform the HTTP body request to a dictionary
- If the HTTP body request is not valid JSON, raise a ``400`` error with the message ``Not a JSON``
- If the dictionary doesn’t contain the key name, raise a ``400`` error with the message ``Missing name``
- Returns the new ``Amenity`` with the status code ``201``

Updates a ``Amenity`` object: ``PUT /api/v1/amenities/<amenity_id>``

- If the ``amenity_id`` is not linked to any ``Amenity`` object, raise a ``404`` error
- You must use ``request.get_json`` from Flask to transform the HTTP body request to a dictionary
- If the HTTP body request is not valid JSON, raise a ``400`` error with the message ``Not a JSON``
- Update the ``Amenity`` object with all key-value pairs of the dictionary.
- Ignore keys: ``id``, ``created_at`` and ``updated_at``
- Returns the ``Amenity`` object with the status code ``200``

__File__
``api/v1/views/amenities.py``, ``api/v1/views/__init__.py``

