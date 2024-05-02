# 0x05. AirBnB clone - RESTful API

## **How to install this repository**

* Clone this repository: `git clone https://github.com/sixthson6/AirBnB_clone_v3`
* Navigate to the directory: `cd AirBnB_clone_v3`
Run the console: `./console`


## **File Descriptions**

[console.py](console.py) - this is the entry point of the command interpreter and the (console) frontend. It currently supports the following:

* `quit`: exits console.
* `create`: creates a new instance of BaseModel and saves it to a filestorage or database (depending on the HBNB_ENV environment variable) and prints the id.
* `update`: Update an instance based on the class name, id, attribute & value
* `show`: Prints an instance as a string based on the class and id
* `all`: Prints string representations of all instances instances
* `destroy`: Deletes an instance based on the class and id"

 ### `models/` - contains the classes used for the AirBnB project. The files in this directory include:

* [base_model.py](/models/base_model.py): this is the base classes all other classes inherit from
* [amenity.py](/models/amenity.py)
* [place.py](/models/place.py)
* [review.py](/models/review.py)
* [city.py](/models/city.py)
* [user.py](/models/city.py)
* [state.py](/models/state.py)

### `models/engine` - contains the filestorage and db_storage classes to handle data storage. The files in this directory include:

 #### [file_storage.py](/models/engine/file_storage.py): serializes instances to a JSON file & deserializes back to instances. contains the following methods:

 * `all`: returns the dictionary __objects
 * `new`: sets in __objects the obj with key <obj class name>.id
 * `save`: serializes __objects to the JSON file (path: __file_path)
 * `reload`: deserializes the JSON file to __objects
 * `delete`: delete obj from __objects if it’s inside
 * `close`: call reload() method for deserializing the JSON file to objects
 * `get`: retrieve an object from the file storage by class and id
 * `count`: count the number of objects in storage matching the given class.

 #### [db_storage.py](/models/engine/db_storage.py): interaacts with the MySQL database. Contains the following methods:

 * `__init__`: Instantiate a DBStorage object
 * `all`: query on the current database session
 * `new`: add the object to the current database session
 * `save`: commit all changes of the current database session
 * `delete`: delete from the current database session obj if not None
 * `reloads`: reloads data from the database
 * `close`: call remove() method on the private session attribute
 * `get`: retrieve an object from the file storage by class and id
 * `count`: count the number of object in storage matching the given class

 ### `test/` - contains all the tests for the AirBnB project. Contains the following tests modules:

 #### `/tests_models/` - contains the tests for the various classes.

 * [/test_models/test_base_model.py](/tests/test_models/test_base_model.py)
 * [/test_models/test_amenity.py](/tests/test_models/test_amenity.py)
 * [/test_models/test_review.py](/tests/test_models/test_review.py)
 * [/test_models/test_amenity.py](/tests/test_models/test_amenity.py)
 * [/test_models/test_place.py](/tests/test_models/test_place.py)
 * [/test_models/test_file_storage.py](/tests/test_models/test_file_storage.py)
 * [/test_models/user.py](/tests/test_models/test_user.py)
 * [/test_models/state.py](/tests/test_models/test_state.py)

 ####  `test/test_console.py` - contains the tests or the console.

 ### `web_flask` - Contains Flask code for creating websites

 #### `/static/` - contains static files
 
 * [/static/images/](/web_flask/static/images/) - conatains images used to render webpages
 * [/static/styles/](/web_flask/static/styles/) - contains css files for styling webpages.

 ### `web_static` - contains HTML code for creating a website.

* [/images/](/web_static/images/) - conatains images used to render webpages
 * [/styles/](/web_static/styles/) - contains css files for styling webpages.

 ## Authors

 ### **inganathi ndinga**  <inganathi2001@gmail.com>
 ### **sumaila sudais ballah**  <sudais2408@gmail.com>

## Example Usage

(hbnb) create BaseModel

bd04e85a-dcff-4567-ab9e-59db2242ac8d

(hbnb) update BaseModel bd04e85a-dcff-4567-ab9e-59db2242ac8d

** attribute name missing **

(hbnb) update BaseModel bd04e85a-dcff-4567-ab9e-59db2242ac8d number_rooms

** value missing **

(hbnb) update BaseModel bd04e85a-dcff-4567-ab9e-59db2242ac8d number_rooms 7

(hbnb) show BaseModel

** instance id missing **

(hbnb) show BaseModel bd04e85a-dcff-4567-ab9e-59db2242ac8d

[BaseModel] (bd04e85a-dcff-4567-ab9e-59db2242ac8d) {'id': 
'bd04e85a-dcff-4567-ab9e-59db2242ac8d', 'created_at': datetime.datetime(2024, 5, 2, 22, 
48, 0, 357643), 'updated_at': datetime.datetime(2024, 5, 2, 22, 49, 12, 654890), 'number_rooms': '7'}

(hbnb) all

[[Amenity] (d25630f0-896d-4ec0-aca1-756eb111f8a9) {'id': 'd25630f0-896d-4ec0-aca1-756eb111f8a9', 'created_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66045), 'updated_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66045)}, [BaseModel] (8e0be3ea-4d3a-4346-a5d6-d35de7b24452) {'id': '8e0be3ea-4d3a-4346-a5d6-d35de7b24452', 'created_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66055), 'updated_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66055)}, [City] (adce53f2-8223-455f-82a4-37fe62978bbe) {'id': 'adce53f2-8223-455f-82a4-37fe62978bbe', 'created_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66067), 'updated_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66067)}, [Place] (e242befa-1b0a-4f89-baa0-97436d8e66c1) {'id': 'e242befa-1b0a-4f89-baa0-97436d8e66c1', 'created_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66077), 'updated_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66077)}, [Review] (67df5204-b98e-4376-ba3b-521fd58cc83c) {'id': '67df5204-b98e-4376-ba3b-521fd58cc83c', 'created_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66087), 'updated_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66087)}, [State] (aeeec64f-fecd-473c-a47f-5a39da87c055) {'id': 'aeeec64f-fecd-473c-a47f-5a39da87c055', 'created_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66098), 'updated_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66098)}, [User] (a097bba3-f3b4-4dff-85c7-f6fe6cfebe87) {'id': 'a097bba3-f3b4-4dff-85c7-f6fe6cfebe87', 'created_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66107), 'updated_at': datetime.datetime(2024, 4, 26, 19, 31, 58, 66107)}, [BaseModel] (bd04e85a-dcff-4567-ab9e-59db2242ac8d) {'id': 'bd04e85a-dcff-4567-ab9e-59db2242ac8d', 'created_at': datetime.datetime(2024, 5, 2, 22, 48, 0, 357643), 'updated_at': datetime.datetime(2024, 5, 2, 22, 49, 12, 654890), 'number_rooms': '7'}]
(hbnb) 

