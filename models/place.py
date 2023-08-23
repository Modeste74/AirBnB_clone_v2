#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from os import getenv


metadata = Base.metadata
place_amenity = Table(
        'place_amenity', metadata,
        Column('place_id', String(60), ForeignKey('places.id'),
            nullable=False, primary_key=True),
        Column('amenity_id', String(60), ForeignKey('amenities.id'),
            nullable=False, primary_key=True)
        )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = relationship(
                'Amenity', secondary='place_amenity',
                viewonly=False, back_populates='place_amenities')
        reviews = relationship(
                'Review', backref='place', cascade='all, delete, delete-orphan')
    else:
        @property
        def reviews(self):
            """Getter attributes for reviews"""
            from models import storage
            review_list = []
            review_objs = storage.all(Review)
            for review in review_objs.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """getter attr for amenities"""
            amenity_list = []
            for amenity_id in self.amenity_ids:
                amenity = storage.get(Amenity, amenity_id)
                if amenity:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """setter attr for amenities"""
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
