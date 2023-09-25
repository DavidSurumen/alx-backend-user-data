#!/usr/bin/env python3
"""
BasicAuth module
"""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    Basic Authentication class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the authorization header
        """
        if not authorization_header or type(authorization_header) is not str:
            return None
        key = authorization_header.split(' ')
        if key[0] != 'Basic':
            return None
        return key[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes base64 string
        """
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) is not str:
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts email and password from authorization header
        """
        if not decoded_base64_authorization_header:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(':')[0]
        pwd = decoded_base64_authorization_header.split(':')[1]
        return (email, pwd)

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """
        Finds a with given credentials
        """
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        try:
            user_objects_list = User.search({'email': user_email})
        except Exception:
            return None

        if not user_objects_list or len(user_objects_list) == 0:
            return None
        if not user_objects_list[0].is_valid_password(user_pwd):
            return None
        return user_objects_list[0]
