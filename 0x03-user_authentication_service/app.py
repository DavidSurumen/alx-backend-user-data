#!/usr/bin/env python3
"""
Simple Flass app
"""
from flask import (
    Flask,
    jsonify,
    request,
)
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Returns a json payload for homepage
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", method=["POST"], strict_slashes=False)
def users() -> str:
    """
    Registers a user
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
