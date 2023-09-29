#!/usr/bin/env python3
"""
Session expiration module
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import (
    datetime,
    timedelta,
)


class SessionExpAuth(SessionAuth):
    """
    Session expiration class
    """
    def __init__(self):
        """ Call base class constructor
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0   # in seconds

    def create_session(self, user_id=None):
        """ (Overloads)
        Creates a session for a user, and assigns duration
        """
        sess_id = super().create_session(user_id)

        if not sess_id:
            return None
        session_dictionary = {"user_id": user_id,
                              "created_at": datetime.now()
                              }
        self.user_id_by_session_id[sess_id] = session_dictionary
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """ (Overloads)
        Retrieves a user ID associated with an active session
        """
        if not session_id:
            return None

        sess_dict = self.user_id_by_session_id.get(session_id)
        if not sess_dict:
            return None
        if self.session_duration <= 0:
            return sess_dict.get('user_id')
        if not sess_dict.get('created_at'):
            return None

        expiry = sess_dict.get('created_at') +\
            timedelta(seconds=self.session_duration)
        if expiry < datetime.now():
            return None

        return sess_dict.get('user_id')
