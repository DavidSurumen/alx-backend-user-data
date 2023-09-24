#!/usr/bin/env python3
"""
BasicAuth module
"""
from .auth import Auth


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
