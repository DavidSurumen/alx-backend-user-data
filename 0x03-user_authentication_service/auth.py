#!/usr/bin/env python3
"""
Task 4 Module -Defines password hashing method
"""
import bcrypt
from db import (
    DB,
    User,
)
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Method hashes a given password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Adds a user to the database
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates login credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                        password.encode("utf-8"),
                        user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        Creates session for a user
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        if user is None:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Finds the user associated with a session id
        """
        if not session_id or type(session_id) is not str:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys an active user session
        """
        if not user_id or type(user_id) is not int:
            raise TypeError('provide an integer user_id')

        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return
        except Exception:
            return

    def get_reset_password_token(self, email: str) -> str:
        """
        Creates a password reset token
        """
        if type(email) is not str:
            raise TypeError('email needs to be a string')

        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            user.reset_token = reset_token
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Resets a user's password
        """
        if type(reset_token) is not str or type(password) is not str:
            raise TypeError('reset_token and password must be strings')

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_hashed_password = _hash_password(password)
            user.hashed_password = new_hashed_password
            user.reset_token = None
            return
        except NoResultFound:
            raise ValueError
