#!/usr/bin/env python3
"""
Authentication
"""

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid


def _hash_password(password: str) -> bytes:
    """
    pwd hashing
    """
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """
    Generats a uuid str
    """
    return str(uuid.uuid4())


class Auth():
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Hashes the pwd and Regesters a new user
        """
        try:
            is_user = self._db.find_user_by(**{"email": email})
            if is_user:
                raise ValueError(f"User {is_user.email} already exists")
        except NoResultFound:
            hash_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hash_pwd)
            return new_user

    def valid_login(self, email: str, password: str):
        """
        chacks for login credentials
        """
        try:
            user = self._db.find_user_by(**{"email": email})
            if user:
                provided_pwd = password.encode("utf-8")
                state = checkpw(provided_pwd, user.hashed_password)
                return state
            else:
                return False
        except (NoResultFound, InvalidRequestError):
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        creates a session
        """
        try:
            user = self._db.find_user_by(**{"email": email})
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
