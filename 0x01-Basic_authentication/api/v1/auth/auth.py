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

        if not path or path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """

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

        Parameters:
            request - flask request object
        """
        return None
