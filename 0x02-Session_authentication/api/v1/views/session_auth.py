#!/usr/bin/env python3
"""
View that handles routes for Session authentication
"""
from api.v1.views import app_views
from flask import (
    request,
    jsonify,
)
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def session_login():
    """ POST /api/v1/auth_session/login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or len(email) < 2:
        return jsonify({"error": "email missing"}), 400
    if not password or len(password) < 2:
        return jsonify({"error": "password missing"}), 400

    user_list = User.search({"email": email})  # expect one user in this list

    if not user_list or len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = user_list[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    session_name = getenv("SESSION_NAME")

    resp = jsonify(user.to_json())
    resp.set_cookie(session_name, session_id)
    return resp


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """ DELETE /api/v1/auth_session/logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
