#!/usr/bin/env python3
"""
This is the db class
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """init"""

        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        adds a user to the db (No validations are required at this stage)
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        print(f"--S--(SAVED): {new_user.email}")

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        This method takes in arbitrary keyword arguments
        and returns the first row found in the users table
        as filtered by the method’s input arguments.
        No validations needed
        """
        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates the user’s attributes as passed in the
        method’s arguments then commit changes to the database.
        """
        user = self.find_user_by(**{"id": user_id})
        for key, val in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, val)
            else:
                raise ValueError
        self._session.commit()
