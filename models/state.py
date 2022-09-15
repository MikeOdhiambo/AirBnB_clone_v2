#!/usr/bin/python3
"""This is the state class"""
import models
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """ Getter attribute for FileStorage environment """
            return [city for city in models.storage.all(City).values() if
                    city.state_id == self.id]
