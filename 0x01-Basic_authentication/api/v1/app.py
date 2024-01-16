#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def filtering_request() -> None:
    """
    Now the biggest piece is the filtering of each request
    """
    path_list = ['/api/v1/status/',
                 '/api/v1/unauthorized/',
                 '/api/v1/forbidden/']

    if auth:
        state = auth.require_auth(request.path, path_list)
        if state is True:
            auths_info = auth.authorization_header(request)
            print(auths_info)
            if auths_info is None:
                abort(401)
            else:
                user = auth.current_user(request)
                print(user)
                if user is None:
                    abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """unauthorized"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbiden(error) -> str:
    """forbiden"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
