#!/usr/bin/env python3
"""
adding Expration date to the session
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Session expiration date
    """

    def __init__(self) -> None:
        """init"""
        super().__init__()
        duration = getenv("SESSION_DURATION", 0)
        try:
            self.session_duration = int(duration)
        except (KeyError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        creating a session
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        returns the user_id given a session id
        """
        try:
            session_dict = self.user_id_by_session_id[session_id]
        except KeyError:
            return None
        if isinstance(session_id, str):

            if self.session_duration <= 0:
                return session_dict.get("user_id", None)

            created_at = session_dict.get("created_at", None)
            duration = timedelta(seconds=self.session_duration)
            if ((created_at + duration) > datetime.now()):
                return session_dict["user_id"]
        return None
