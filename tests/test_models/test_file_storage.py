import unittest
from unittest.mock import patch
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        del_list = []
        for key in FileStorage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del FileStorage._FileStorage__objects[key]

    @classmethod
    def tearDownClass(cls):
        """Remove created test objects"""
        del_list = []
        for key in FileStorage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del FileStorage._FileStorage__objects[key]

    def setUp(self):
        """Set up test environment"""
        pass

    def tearDown(self):
        """Remove created test objects"""
        del_list = []
        for key in FileStorage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del FileStorage._FileStorage__objects[key]

    def test_obj_list_empty(self):
        """__objects is initially empty"""
        self.assertEqual(FileStorage._FileStorage__objects, {})

    def test_new(self):
        """New object is correctly added to __objects"""
        new = BaseModel()
        FileStorage.new(new)
        self.assertIn(str(type(new).__name__) + '.' + str(new.id), FileStorage._FileStorage__objects)

    def test_all(self):
        """__objects is properly returned"""
        new = BaseModel()
        FileStorage.new(new)
        self.assertEqual(FileStorage.all(), {str(type(new).__name__) + '.' + str(new.id): new})

    def test_save(self):
        """File is not created on BaseModel save"""
        new = BaseModel()
        FileStorage.new(new)
        FileStorage.save()
        with open(FileStorage._FileStorage__file_path, 'r') as f:
            self.assertEqual(f.read(), '{}')

    def test_reload(self):
        """Storage file is successfully loaded to __objects"""
        new = BaseModel()
        FileStorage.new(new)
        FileStorage.save()
        FileStorage.reload()
        for obj in FileStorage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """Load from an empty file"""
        FileStorage.reload()
        self.assertEqual(FileStorage._FileStorage__objects, {})

    def test_reload_from_nonexistent(self):
        """Nothing happens if file does not exist"""
        with patch('builtins.open', side_effect=lambda *args: None) as mock_open:
            FileStorage.reload()
            mock_open.assert_called_once_with(FileStorage._FileStorage__file_path, 'r')

    def test_type_path(self):
        """Confirm __file_path is string"""
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def test_type_objects(self):
        """Confirm __objects is a dict"""
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_key_format(self):
        """Key is properly formatted"""
        new = BaseModel()
        FileStorage.new(new)
        self.assertIn(str(type(new).__name__) + '.' + str(new.id), FileStorage._FileStorage__objects)

    def test_storage_var_created(self):
        """FileStorage object storage created"""
        self.assertIsInstance(FileStorage(), FileStorage)


if __name__ == '__main__':
    unittest.main()


