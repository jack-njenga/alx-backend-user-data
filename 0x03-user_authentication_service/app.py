#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    index page
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    users page
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        new_user = AUTH.register_user(email, password)
        result = {"email": new_user.email, "message": "user created"}
        return jsonify(result)
    except ValueError:
        return jsonify({"message": "email already regestered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
