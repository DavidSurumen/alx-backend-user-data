#!/usr/bin/env python3
"""
Session authentication module
"""
from .auth import Auth
import uuid
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """ Session authentication class
    """
    user_id_by_session_id = {}    # { <session ID> : <user ID> }

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session id for a user id
        """
        if not user_id or type(user_id) is not str:
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Gets a user associated with a session
        """
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overrides Auth.current_user.
        Retrieves a user instance associated with a session.
        """
        session_id = self.session_cookie(request)
        return User.get(self.user_id_for_session_id(session_id))

    def destroy_session(self, request=None) -> bool:
        """
        Logs a user out by destroying the session
        """
        if not request:
            return None
        session_cookie = self.session_cookie(request)
        if session_cookie:
            user_id = self.user_id_for_session_id(session_cookie)
            if user_id:
                del self.user_id_by_session_id[session_cookie]
                return True
        return False
