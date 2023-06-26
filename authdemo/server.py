import base64
import hmac
import hashlib
import json
from typing import Optional
from fastapi import FastAPI, Cookie
from fastapi.params import Body
from fastapi.responses import Response


app = FastAPI() # экземпляр приложения fastapi

SECRET_KEY = '5fce4da39635b1607eab5f38e82ccc39d852646773882dba7ffe194d3a94ca33'
PASSWORD_SALT = "078750f9429d7bd04959977ff3ced4ce8abc1802fe8a9e6f628342b6c4016d93"


def sign_data(data):
    """Возвращает подписаные даные data"""
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
        ).hexdigest().upper()


users = {
        "svatoslav@user.com": {
            "name": "Святослав",
            "password": "8558bf2d0647732e702ac6a45391a20f241ba447b9ce76a1387cfa530c8a1bea",
            "balance": 100_000
            },
        "oleg@user.com": {
            "name": "Олег",
            "password": "b863e4fb5710490399293e4fee7edfb8d93524e7042548bf53a29cb500d22a9a",
            "balance": 20_000
            }
        }


def get_username_from_signed_string(username_signed):
    username_base64, sign = username_signed.split(".")
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username


def verify_password(username, password):
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    stored_password_hash = users[username]['password']
    return password_hash == stored_password_hash


@app.get("/")
def index_page(username: Optional[str] = Cookie(default=None)):
    """Индексная страничка приложения"""
    with open("./templates/login.html", "r") as f:
        login_page = f.read()
    if not username:
        return Response(login_page, media_type="text/html")
    valid_username = get_username_from_signed_string(username)
    if not valid_username:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response
    try:
        user = users[valid_username]
    except KeyError:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key="username")
        return response
    return Response(f"Привет {users[valid_username]['name']}!<br>Баланс: {users[valid_username]['balance']}",
                        media_type="text/html")# media_type устанавливает http заголовок content_type (utf-8 по умолчанию) 


@app.post("/login")
def process_login_page(data: dict = Body(...)):
    username = data["username"]
    password = data["password"]
    user = users.get(username)
    if not user or not verify_password(username, password):
        return Response(
            json.dumps({
                "success": False,
                "message": "Я вас не знаю!!!"
                }),
            media_type="application/json")
    else:
        response = Response(
            json.dumps({
                "success": True,
                "message": f"Привет, {user['name']}!<br>Ваш баланс: {user['balance']}"
                }),
            media_type="application/json")
        username_signed = base64.b64encode(username.encode()).decode() + "." + sign_data(username)
        response.set_cookie(key="username", value=username_signed)
        return response
