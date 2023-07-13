#!/usr/bin/env python3
"""Test Module for BaseModel

This is the test module for BaseModel on which other
Models will be based
"""

import uuid
import io
from unittest import TestCase, mock
from datetime import datetime
import time
from models.base_model import BaseModel


class BaseModelTestClass(TestCase):
    def test_id_is_string(self):
        """Tests if id is of type string
        """
        model = BaseModel()
        self.assertIsInstance(model.id, str)
        self.assertTrue(len(model.id.strip()) > 0)

    def test_id_is_unique(self):
        """Tests that id is unique for each instance of BaseClass
        """
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model2.id, model1.id)

    def test_created_at_is_datetime_object(self):
        """Tests if the created_at property is of type datetime
        """
        model = BaseModel()
        self.assertIsInstance(model.created_at, datetime)

    def test_updated_at(self):
        model = BaseModel()
        updated_at = model.updated_at
        self.assertIsInstance(updated_at, datetime)
        model.save()
        self.assertGreater(model.updated_at, updated_at)

    def test_save_method(self):
        model = BaseModel()
        old_updated_at = model.updated_at
        self.assertEqual(model.created_at, old_updated_at)
        model.save()
        self.assertGreater(model.updated_at, old_updated_at)

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_string_representation(self, mock_stdout):
        model = BaseModel()
        print(model, end='')
        self.assertEqual(
                mock_stdout.getvalue(),
                '[BaseModel] ({}) {}'.format(
                    model.id, model.__dict__))

    def test_to_dict_returns_dictionary(self):
        model = BaseModel()
        self.assertIsInstance(model.to_dict(), dict)

    def test_to_dict_with_argument(self):
        """Test that to_dict with argument

        to_dict method should throw exception
        when called with arguments
        """
        model = BaseModel()
        with self.assertRaises(Exception):
            model.to_dict(5)

    def test_to_dict_returns_correct_values(self):
        """ Test that all contents of to_dict are as expected
        """
        model = BaseModel()
        model_dict = {key: value for key, value in model.__dict__.items()}

        model_dict['created_at'] = model_dict['created_at'].isoformat()
        model_dict['updated_at'] = model_dict['updated_at'].isoformat()

        model_dict['__class__'] = type(model).__name__
        self.assertEqual(model.to_dict(), model_dict)

    def test_to_dict_updated_created_at_is_string(self):
        """Test that the created_at and updated_at formate in to_dict is str
        """
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict["created_at"], str)
        self.assertIsInstance(model_dict["updated_at"], str)

    def test_create_instance_from_to_dict(self):
        """Test creation of instance from to_dict
        """
        model = BaseModel()
        data = {}
        model2 = BaseModel(**data)
        self.assertFalse(model.id == model2.id)
        self.assertFalse(model.created_at == model2.created_at)
        self.assertFalse(model.updated_at == model2.updated_at)
        model3_data = {
                key: val for key, val
                in model.to_dict().items()
                if key != '__class__'}
        model3 = BaseModel(**model3_data)
        self.assertTrue(model.id == model3.id)
        self.assertTrue(model.updated_at == model3.updated_at)
        self.assertTrue(model.created_at == model3.created_at)
    def test_incomplete_kwargs_throw_error(self):
        model = BaseModel()
        with self.assertRaises(Exception):
            model2_data = model.to_dict()
            del model2_data["created_at"]
            model2 = BaseModel(**model2_data)
