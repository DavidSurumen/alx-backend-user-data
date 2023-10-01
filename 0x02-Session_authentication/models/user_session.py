#!/usr/bin/env python3
"""
Module for session authentication, with session data
persisted in file system
"""
from models.base import Base


class UserSession(Base):
    """ User session class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a user
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
