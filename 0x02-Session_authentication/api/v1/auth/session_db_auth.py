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
        session_id = super().create_session(user_id)
        self.save_to_file(session_id)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ (Overloads)
        Retrieves user ID by requesting UserSession in the database
        based on session_id.
        Return:
            user_id (str)
        """
        self.load_from_file()
        sess_dct = self.user_id_by_session_id.get(session_id)
        if sess_dct:
            if self.session_duration <= 0:
                return sess_dct.get('user_id')
            if sess_dct.get('created_at'):
                expiry = sess_dct.get('created_at') +\
                        timedelta(seconds=self.session_duration)
                if expiry >= datetime.now():
                    return sess_dct.get('user_id')

    def destroy_session(self, request=None):
        """ (Overloads)
        Destroys the UserSession based on the session ID from the request
        cookie.
        """
        if not request:
            return None
        sess_id = self.session_cookie(request)
        if sess_id:
            user_id = self.user_id_for_session_id(sess_id)
            if user_id:
                del self.user_id_by_session_id[sess_id]
                self.save_to_file()
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
