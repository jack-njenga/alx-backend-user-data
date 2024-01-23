#!/usr/bin/env python3
"""
Entry Point
"""
import requests

url = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    user registration
    """
    data = {"email": email, "password": password}
    response = requests.post(f"{url}/users", data=data)
    # print(response.content)
    assert (response.status_code == 200)
    # print(response.json())
    assert (response.json() == {"email": email, "message": "user created"})

    response = requests.post(f"{url}/users", data=data)
    assert (response.status_code == 400)
    assert (response.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """ wrong pwd login test"""
    data = {'email': email, 'password': password}
    response = requests.post(f"{url}/sessions", data=data)
    assert (response.status_code == 401)


def profile_unlogged() -> None:
    """ profile unlogged """
    response = requests.get(f"{url}/profile")
    assert (response.status_code == 403)


def log_in(email: str, password: str) -> str:
    """ corrct pwd login test """
    data = {'email': email, 'password': password}
    response = requests.post(f"{url}/sessions", data=data)

    assert (response.status_code == 200)
    assert (response.json() == {"email": email,
                                "message": "logged in"})
    assert ('session_id' in response.cookies)
    session_id = response.cookies.get('session_id')
    return session_id


def profile_logged(session_id: str) -> None:
    """ loggin user test """
    cookie = {'session_id': session_id}
    response = requests.get(f"{url}/profile", cookies=cookie)
    assert (response.status_code == 200)
    assert ('email' in response.json())


def log_out(session_id: str) -> None:
    """ user logout test """
    cookie = {'session_id': session_id}
    response = requests.delete(f"{url}/sessions", cookies=cookie)
    assert (response.status_code == 200)
    assert (response.json() == {"message": "Bienvenue"})


def reset_password_token(email: str) -> str:
    """ reset pwd test """
    response = requests.post(f"{url}/reset_password",
                             data={'email': email})
    assert (response.status_code == 200)
    assert ('email' in response.json())
    assert (response.json()["email"] == email)
    assert ('reset_token' in response.json())
    token = response.json().get('reset_token')
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ pwd update test """
    data = {
        "email": email,
        "new_password": new_password,
        "reset_token": reset_token}
    response = requests.put(f"{url}/reset_password", data=data)
    assert (response.status_code == 200)
    assert (response.json() == {"email": email,
                                "message": "Password updated"})


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

    # print(":)")
