#!/usr/bin/env
"""
Password hashing module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
