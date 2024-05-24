
# HolbertonBnB Console

HolbertonBnB Console is a command-line interface (CLI) application that allows users to interact with objects stored in a data storage system. It provides functionalities for creating, displaying, updating, and deleting instances of various classes such as User, State, City, Amenity, Place, Review, etc.

## Installation

To use the HolbertonBnB Console, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Ashraf-Atef1/AirBnB_clone_v2.git
   ```
2. Navigate to the project directory:

   ```bash
   cd holberton-bnb
   ```
3. Run the console:

   ```bash
   ./console.py
   ```

## Usage

The HolbertonBnB Console supports the following commands:

- `create`: Create a new instance of a class and save it to the data storage.

  ```
  create <class_name>
  ```
- `show`: Display the string representation of an instance based on the class name and id.

  ```
  show <class_name> <instance_id>
  ```
- `destroy`: Delete an instance based on the class name and id.

  ```
  destroy <class_name> <instance_id>
  ```
- `all`: Display the string representation of all instances or all instances of a specific class.

  ```
  all [<class_name>]
  ```
- `update`: Update an instance attribute based on the class name and id.

  ```
  update <class_name> <instance_id> <attribute_name> "<attribute_value>"
  ```
- `quit` or `EOF`: Exit the console.

## Supported Classes

The HolbertonBnB Console supports the following classes:

- BaseModel
- User
- State
- City
- Amenity
- Place
- Review

## Data Storage

The application uses a JSON file (`file.json`) as the default data storage system. Instances are serialized to JSON format and stored in this file. You can switch to a database storage system by setting the environmental variable `HBNB_TYPE_STORAGE` to `db`.

## Contributions

Contributions are welcome! If you find any issues or would like to contribute to the project, please open an issue or create a pull request on the [GitHub repository](https://github.com/your_username/holberton-bnb).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize the README file according to your project's specific details and requirements.
