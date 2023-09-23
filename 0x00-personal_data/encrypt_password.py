#!/usr/bin/env python3
"""
Password hashing module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
