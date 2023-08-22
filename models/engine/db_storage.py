#!/usr/bin/python3
"""define a storage engine"""

from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """database storage engine class"""
    __engine = None
    __session = None

    def __init__(self):
        """initializes the database storage engine"""
        user = environ.get('HBNB_MYSQL_USER')
        password = environ.get('HBNB_MYSQL_PWD')
        host = environ.get('HBNB_MYSQL_HOST')
        db = environ.get('HBNB_MYSQL_DB')
        self.__engine = create_engine(
                f'mysql+mysqldb://{user}:{password}@{host}:3306/{db}',
                pool_pre_ping=True)
        if environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        """Queries all objs in database"""
        classes = (User, City, Place, State, Amenity, Review)
        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for cls in classes:
                objs.extend(self.__session.query(cls).all())
        obj_dict = {}
        for obj in objs:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            obj_dict[key] =obj
        return obj_dict

    def new(self, obj):
        """adds a new object to the database"""
        self.__session.add(obj)

    def save(self):
        """commits all changes to the db"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from the database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create tables and new sessions"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()
