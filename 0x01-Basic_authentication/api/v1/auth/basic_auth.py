#!/usr/bin/env python3
"""
Basic Auth system
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    basic auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header
        """
        if authorization_header:
            if type(authorization_header) is str:
                # print(f"{authorization_header[:6]} == Basic ")
                if authorization_header[:6] == "Basic ":
                    return authorization_header.replace("Basic ", "")
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64 string
        """
        if base64_authorization_header:
            if type(base64_authorization_header) is str:
                try:
                    decstr = b64decode(
                        base64_authorization_header,
                        validate=True)
                    decstr = decstr.decode('utf-8')
                    return decstr
                except Exception as e:
                    return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header:
            if type(decoded_base64_authorization_header) is str:
                if ":" in decoded_base64_authorization_header:
                    email = decoded_base64_authorization_header.split(":")[0]
                    pwd = decoded_base64_authorization_header.split(":")[-1]
                    return email, pwd
        return None, None

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            user = User.search({"email": user_email})[0]
            if user.is_valid_password(user_pwd):
                return user
        except (KeyError, IndexError):
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Auth and retrieves the User instance for a request
        """

        auth_header = self.authorization_header(request)
        b64header = self.extract_base64_authorization_header(auth_header)
        decheader = self.decode_base64_authorization_header(b64header)
        email, pwd = self.extract_user_credentials(decheader)
        # print(f"{auth_header}")
        # print(f"{b64header}")
        # print(f"{decheader}")
        # print(f"{email}, {pwd}")

        return self.user_object_from_credentials(email, pwd)
