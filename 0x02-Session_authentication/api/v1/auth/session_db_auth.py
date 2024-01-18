#!/usr/bin/env python3
"""
Saving the session in db
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Session db class
    """

    def create_session(self, user_id=None):
        """
        creates and stores new instance of UserSession and
        returns the Session ID
        """
        session_id = super().create_session(user_id)
        if session_id:
            session_dict = {
                "user_id": user_id,
                "session_id": session_id
            }
            session = UserSession(**session_dict)
            session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        overload
        """
        try:
            session = UserSession.search({'session_id': session_id})[0]
        except KeyError:
            return None
        if isinstance(session_id, str):
            if self.session_duration <= 0:
                return session.user_id
            duration = timedelta(seconds=self.session_duration)
            if ((session.created_at + duration) > datetime.utcnow()):
                return session.user_id
        return None

    def destroy_session(self, request=None):
        """
        overload
        """
        session_id = self.session_cookie(request)
        try:
            session = UserSession.search({'session_id': session_id})[0]
            session.remove()
            return True
        except (KeyError, IndexError):
            return False
