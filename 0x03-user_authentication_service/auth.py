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
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except (NoResultFound, InvalidRequestError):
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

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        takes a single session_id string argument and
        returns the corresponding User or None
        """
        if session_id:
            try:
                user = self._db.find_user_by(**{"session_id": str(session_id)})
                return user
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: str) -> None:
        """
        Destroys a users session
        """
        try:
            self._db.update_user(user_id, **{"session_id": None})
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Returns the reset token
        """
        try:
            user = self._db.find_user_by(**{"email": email})
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        updates the users pwd
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            kwargs = {
                "hashed_password": _hash_password(password),
                "reset_token": None}
            self._db.update_user(user.id, **kwargs)
        except NoResultFound:
            raise ValueError
