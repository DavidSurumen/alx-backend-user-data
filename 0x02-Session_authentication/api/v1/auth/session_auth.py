#!/usr/bin/env python3
"""
Session authentication module
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """ Session authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session id for a user id
        """
        if not user_id or type(user_id) is not str:
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id
