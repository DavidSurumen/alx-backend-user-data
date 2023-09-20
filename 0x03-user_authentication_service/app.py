#!/usr/bin/env python3
"""
Simple Flass app
"""
from flask import (
    Flask,
    jsonify,
    request,
    abort,
    make_response,
    redirect,
    url_for,
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


@app.route("/users", methods=["POST"], strict_slashes=False)
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


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """
    Logs in an existing user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401, 'email or password is not provided in the request')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response(jsonify({'email': "{}".format(email),
                                      'message': "logged in"
                                      }))
        resp.set_cookie('session_id', session_id)
        return resp
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logs out an active user
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403, 'no session id in cookie')

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Returns the profile an active user
    """
    session_id = request.cookies.get("session_id")

    if not session_id:
        abort(403, 'no session id in cookie')

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({'email': "{}".format(user.email)})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    Handles reset password requests.
    Returns a password reset token
    """
    email = request.form.get("email")
    if not email:
        abort(403, 'must provide an email to reset password')

    try:
        user = AUTH.get_reset_password_token(email)
        return jsonify({
                            'email': "{}".format(email),
                            'reset_token': "{}".format(user.reset_token)
                        })
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
