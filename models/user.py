#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from os import getenv


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship('Place', back_reference='user', cascade="all, delete, delete-orphan")
        Review = relationship('Review', back_reference='user', cascade="all, delete, delete-orphan")
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
