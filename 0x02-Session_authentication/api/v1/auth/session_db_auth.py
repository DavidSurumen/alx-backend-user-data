#!/usr/bin/env python3
""" Session authentication module with persistence
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
import json
from os import path
from datetime import (
    datetime,
    timedelta,
)
from models.user_session import UserSession


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


class SessionDBAuth(SessionExpAuth):
    """ Session authentication class
    """
    def create_session(self, user_id=None):
        """ (Overloads)
        Create and store new instances of UserSession
        Return:
            session ID (str)
        """
        if not user_id or type(user_id) is not str:
            return
        session_id = super().create_session(user_id)
        user_session = UserSession()
        user_session.user_id = user_id
        user_session.session_id = session_id
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ (Overloads)
        Retrieves user ID by requesting UserSession in the database
        based on session_id.
        Return:
            user_id (str)
        """
        if not session_id:
            return

        UserSession.load_from_file()
        all_objs = UserSession.all()

        for obj in all_objs:
            if obj.session_id == session_id:
                return obj.user_id
        return

    def destroy_session(self, request=None):
        """ (Overloads)
        Destroys the UserSession based on the session ID from the request
        cookie.
        """
        if not request:
            return None
        sess_id = self.session_cookie(request)
        if sess_id:
            sess_objs_list = UserSession.search(session_id=sess_id)
            if len(sess_obj_list) > 0:
                sess_obj_list[0].remove()
                return True
        return False

    def save_to_file(self, session_id=None):
        """ Saves the session_ID-user_ID dictionary to a file
        """
        filepath = ".db_session.json"
        if not session_id:
            return
        session_data = self.user_id_by_session_id
        sess_dct = session_data[session_id]
        for key, val in sess_dct.items():
            if type(val) is datetime:
                session_data[session_id][key] = val.strftime(TIMESTAMP_FORMAT)

        with open(filepath, 'w') as f:
            json.dump(session_data, f)

    def load_from_file(self):
        """ Loads session data from file
        """
        filepath = ".db_session.json"
        if path.exists(filepath):
            with open(filepath, 'r') as f:
                loaded_sess_data = json.load(f)
            for key, val in loaded_sess_data.items():
                for k, v in val.items():
                    if k == 'created_at':
                        loaded_sess_data[key][k] =\
                                datetime.strptime(v, TIMESTAMP_FORMAT)
            self.user_id_by_session_id = loaded_sess_data
