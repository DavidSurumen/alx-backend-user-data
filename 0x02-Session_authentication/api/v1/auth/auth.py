#!/usr/bin/env python3
"""
API Authentication module
"""
from flask import (
    request,
)
from typing import (
    List,
    TypeVar,
)
import re
import os


class Auth:
    """
    Auth routines
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks whether authentication is required

        Return:
            True -> If path is not in excluded_paths, or path is None, or
                    excluded_list is None, authenticate.

            False -> If path is in excluded_paths, no authentication.
        """
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if path and path.split('/')[-1] != '':
            path = path + '/'

        for ex_path in excluded_paths:
            pattern = ''
            if ex_path[-1] == '*':
                pattern = '{}.*'.format(ex_path[0:-1])
                if re.match(pattern, path):
                    return False
            if path == ex_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization key from request header
        Parameters:
            request - flask request object
        """
        if not request:
            return None
        auth_key = request.headers.get('Authorization')
        if not auth_key:
            return None
        return auth_key

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves a user object
        Parameters:
            request - flask request object
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves a cookie value from a request, as session ID.
        """
        if not request:
            return None
        cookie = os.getenv("SESSION_NAME")
        return request.cookies.get(cookie)
