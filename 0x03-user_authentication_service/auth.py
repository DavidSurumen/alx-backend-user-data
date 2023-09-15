#!/usr/bin/env python3
"""
Task 4 Module -Defines password hashing method
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Method hashes a given password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
