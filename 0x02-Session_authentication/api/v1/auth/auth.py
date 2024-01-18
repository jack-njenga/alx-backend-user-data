#!/usr/bin/env python3
"""
All Authentication systems
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    Auth class
    """
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """
        check if we require Authentication or not
        """
        if path and excluded_paths:
            if path[-1] == "/":
                path = path[:-1]
            if "*" in path:
                path = path.split("*")[0]
            for epath in excluded_paths:
                if (path in epath) or (epath in path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Auth headers"""
        if request is not None:
            auths = request.headers.get("Authorization", None)
            return auths
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ get current user"""
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request
        """
        if request:
            session_name = getenv("SESSION_NAME")
            return request.cookies.get(session_name, None)
        return None
