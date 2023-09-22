#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
"""from models.city import City"""
from sqlalchemy.orm import relationship
from os import environ
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship('City', cascade='all, delete-orphan', backref='state')

    if environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """return list of city instances with
            state_id == current state.id"""
            from models import storage
            cities_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
