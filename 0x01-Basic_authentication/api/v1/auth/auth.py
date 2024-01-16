#!/usr/bin/env python3
"""
All Authentication systems
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class
    """

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """..."""
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
        """..."""
        if request is not None:
            auths = request.headers.get("Authorization", None)
            return auths
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """..."""
        # auth_header = self.authorization_header(request)
        return None
