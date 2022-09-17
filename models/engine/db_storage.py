#!/usr/bin/python3
"""This is the dbstorage class for AirBnB"""
import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import models
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {'City': City, 'State': State, 'User': User,
           'Amenitiy': Amenity, 'Place': Place,
           'Review': Review}


class DBStorage:
    """This class storages in the database to instances
    """
    __engine = None
    __session = None

    def __init__(self):
        """ Instantiation of DBStorage class """
        try:
            self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                os.getenv("HBNB_MYSQL_USER"), os.getenv("HBNB_MYSQL_PWD"),
                os.getenv("HBNB_MYSQL_HOST"), os.getenv("HBNB_MYSQL_DB")),
                pool_pre_ping=True)
        except Exception:
            pass

        self.__session = sessionmaker(self.__engine)()

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def __del__(self):
        """ close session """
        self.__session.close()

    def all(self, cls=None):
        """ all """
        objects = {}
        for clase in classes:
            if cls is None or cls is classes[clase] or cls is clase:
                current = self.__session.query(classes[clase]).all()
                for obj in current:
                    key = obj.__class__.__name__ + '.' + obj.id
                    objects[key] = obj
        return objects

    def new(self, obj):
        """ add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session """
        try:
            self.__session.commit()
        except Exception:
            self.__session.rollback()

    def delete(self, obj=None):
        """ delete from the current database session obj if not None """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database
            create the current database session """
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session

    def close(self):
        """ call remove() method on the private session attribute """
        self.__session.remove()
