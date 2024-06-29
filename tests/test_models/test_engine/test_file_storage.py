#!/usr/bin/python3
"""Module for testing FileStorage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os


class TestFileStorage(unittest.TestCase):
    """Class to test the FileStorage methods"""

    def setUp(self):
        """Set up the test environment"""
        # Clear all objects in storage
        del_list = list(storage.all().keys())
        for key in del_list:
            del storage.all()[key]

    def tearDown(self):
        """Remove the storage file at the end of tests"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass  # File does not exist, so nothing to clean up

    def test_obj_list_empty(self):
        """__objects is initially empty"""
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """New object is correctly added to __objects"""
        new = BaseModel()
        all_objects = storage.all()
        obj = list(all_objects.values())[-1]  # Get the last object added
        self.assertTrue(new is obj)

    def test_all(self):
        """__objects is properly returned"""
        new = BaseModel()
        all_objects = storage.all()
        self.assertIsInstance(all_objects, dict)
        self.assertIn(f'BaseModel.{new.id}', all_objects)

    def test_base_model_instantiation(self):
        """File is not created on BaseModel save"""
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """Data is saved to file"""
        new = BaseModel()
        dict_repr = new.to_dict()
        new.save()
        new2 = BaseModel(**dict_repr)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """FileStorage save method"""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """Storage file is successfully loaded to __objects"""
        new = BaseModel()
        new.save()
        storage.reload()
        all_objects = storage.all()
        loaded = list(all_objects.values())[-1]
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """Load from an empty file"""
        with open('file.json', 'w') as f:
            pass  # Create an empty file
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """Nothing happens if the file does not exist"""
        os.remove('file.json')  # Ensure file does not exist
        self.assertIsNone(storage.reload())

    def test_base_model_save(self):
        """BaseModel save method calls storage save"""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """Confirm __file_path is string"""
        self.assertIsInstance(storage._FileStorage__file_path, str)

    def test_type_objects(self):
        """Confirm __objects is a dict"""
        self.assertIsInstance(storage.all(), dict)

    def test_key_format(self):
        """Key is properly formatted"""
        new = BaseModel()
        _id = new.to_dict()['id']
        new.save()  # Save to ensure the key is created
        last_key = list(storage.all().keys())[-1]  # Get the last key
        self.assertEqual(last_key, f'BaseModel.{_id}')

    def test_storage_var_created(self):
        """FileStorage object storage created"""
        from models.engine.file_storage import FileStorage
        self.assertIsInstance(storage, FileStorage)


if __name__ == '__main__':
    unittest.main()
