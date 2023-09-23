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
