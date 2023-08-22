#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import environ
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage


storage_type = environ.get('HBNB_TYPE_STORAGE')
if storage_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
