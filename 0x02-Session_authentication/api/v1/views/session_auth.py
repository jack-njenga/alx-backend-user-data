#!/usr/bin/env python3
"""
Handles all the routes for the Session authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from os import getenv
from models.user import User
from api.v1.app import auth


@app_views.route("/auth_session/login",
                 methods=["POST"],
                 strict_slashes=False)
def login():
    """
    login route
    """
    email = request.form.get("email", None)
    pwd = request.form.get("password", None)
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if pwd is None:
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({'email': email})[0]
        if user.is_valid_password(pwd):
            sess = getenv("SESSION_NAME")
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(sess, session_id)

            return response
        else:
            return jsonify({"error": "wrong password"}), 401
    except (KeyError, IndexError):
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route("/auth_session/logout",
                 methods=["DELETE"],
                 strict_slashes=False)
def logout():
    """
    logging out now
    """
    destroyed = auth.destroy_session(request)
    if destroyed is True:
        return jsonify({}), 200
    else:
        abort(404)
