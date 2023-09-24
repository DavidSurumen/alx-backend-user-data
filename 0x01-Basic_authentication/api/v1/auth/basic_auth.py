#!/usr/bin/env python3
"""
BasicAuth module
"""
from .auth import Auth
import base64


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
