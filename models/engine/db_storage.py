#!/usr/bin/python3
""" This is the DBStorage class """

import os
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime


class DBStorage:
    """ Custom class for DBStorage """
    __engine = None
    __session = None

    def __init__(self):
        """ Initialization method """
        user = os.getenv('HBNB_MYSQL_USER')
        psw = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, psw, host, db, pool_pre_ping=True))
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ Method returns all objects of a certain type, or all objects """

        classes = [City, State, User, Place, Review, Amenity]
        objs = []
        if cls:
            objs = self.__session.query(eval(cls))
        else:
            for curr in classes:
                objs.extend([obj for obj in self.__session.query(curr).all()])
        objs_dict = {"{}.{}".format(type(obj).__name__, obj.id):
                     obj for obj in objs}
        return objs_dict

    def new(self, obj):
        """ Method adds an object to the current session

        Arguments:
            obj: object to add
        """
        self.__session.add(obj)

    def save(self):
        """ Method saves (commits) all changes in the current session """
        try:
            self.__session.commit()
        except:
            self.__session.rollback()

    def delete(self, obj=None):
        """ Method deletes an object from the current session

        Arguments:
            obj: object to delete
        """
        self.__session.delete(obj)

    def close(self):
        """ Call remove method on private session attribute """
        self.__session.close()

    def reload(self):
        """ Method creates a database session and all tables """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def classes(self):
        """Returns a dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def attributes(self):
        """Returns the valid attributes and their types for classname."""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes
