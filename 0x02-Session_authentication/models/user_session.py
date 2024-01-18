#!/usr/bin/env python3
"""
User Session system
"""
from models.base import Base


class UserSession(Base):
    """
    User Session class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        init
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id", None)
        self.session_id = kwargs.get("session_id", None)
