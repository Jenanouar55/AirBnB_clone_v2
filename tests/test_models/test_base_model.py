#!/usr/bin/python3
"""Test cases for BaseModel class"""
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel"""

    def __init__(self, *args, **kwargs):
        """Initialize the test class"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """Set up test environment"""
        pass

    def tearDown(self):
        """Tear down test environment"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass  # File does not exist, so nothing to clean up

    def test_default(self):
        """Test default instance creation"""
        instance = self.value()
        self.assertIsInstance(instance, self.value)

    def test_kwargs(self):
        """Test instantiation with **kwargs"""
        instance = self.value()
        copy = instance.to_dict()
        new_instance = BaseModel(**copy)
        self.assertFalse(new_instance is instance)

    def test_kwargs_int(self):
        """Test instantiation with invalid **kwargs key"""
        instance = self.value()
        copy = instance.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            BaseModel(**copy)

    def test_save(self):
        """Test save method"""
        instance = self.value()
        instance.save()
        key = f"{self.name}.{instance.id}"
        with open('file.json', 'r') as f:
            data = json.load(f)
            self.assertEqual(data[key], instance.to_dict())

    def test_str(self):
        """Test string representation"""
        instance = self.value()
        expected_str = f'[{self.name}] ({instance.id}) {instance.__dict__}'
        self.assertEqual(str(instance), expected_str)

    def test_todict(self):
        """Test to_dict method"""
        instance = self.value()
        dict_repr = instance.to_dict()
        self.assertEqual(instance.to_dict(), dict_repr)

    def test_kwargs_none(self):
        """Test instantiation with None as key"""
        with self.assertRaises(TypeError):
            BaseModel(**{None: None})

    def test_kwargs_one(self):
        """Test instantiation with invalid key"""
        with self.assertRaises(KeyError):
            BaseModel(**{'Name': 'test'})

    def test_id(self):
        """Test id attribute"""
        instance = self.value()
        self.assertIsInstance(instance.id, str)
        try:
            UUID(instance.id, version=4)
        except ValueError:
            self.fail(f"Invalid UUID4 format for id: {instance.id}")

    def test_created_at(self):
        """Test created_at attribute"""
        instance = self.value()
        self.assertIsInstance(instance.created_at, datetime.datetime)

    def test_updated_at(self):
        """Test updated_at attribute"""
        instance = self.value()
        self.assertIsInstance(instance.updated_at, datetime.datetime)
        dict_repr = instance.to_dict()
        new_instance = BaseModel(**dict_repr)
        self.assertFalse(new_instance.created_at == new_instance.updated_at)


if __name__ == '__main__':
    unittest.main()
