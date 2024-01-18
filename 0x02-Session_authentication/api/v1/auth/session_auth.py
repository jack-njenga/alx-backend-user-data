#!/usr/bin/env python3
"""
Session auth system
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    Session Auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id:
        """
        if user_id:
            if type(user_id) is str:
                session_id = str(uuid4())
                self.user_id_by_session_id[session_id] = user_id
                return self.user_id_by_session_id
        return None
