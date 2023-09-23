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
        """
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if path.split('/')[-1] != '':
            path = path + '/'

        if not path or path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """

        Parameters:
            request - flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """

        Parameters:
            request - flask request object
        """
        return None
