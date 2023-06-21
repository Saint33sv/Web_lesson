import base64
import hmac
import hashlib
from typing import Optional
from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response


app = FastAPI() # экземпляр приложения fastapi

SECRET_KEY = '5fce4da39635b1607eab5f38e82ccc39d852646773882dba7ffe194d3a94ca33'


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
            "password": "1234",
            "balance": 100_000
            },
        "oleg@user.com": {
            "name": "Олег",
            "password": "12345",
            "balance": 20_000
            }
        }


def get_username_from_signed_string(username_signed):
    username_base64, sign = username_signed.split(".")
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username


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
    return Response(f"Привет {users[valid_username]['name']}!",
                        media_type="text/html")# media_type устанавливает http заголовок content_type (utf-8 по умолчанию) 


@app.post("/login")
def process_login_page(login=Form(...), password=Form(...)):
    user = users.get(login)
    if not user or user["password"] != password:
        return Response("Я вас не знаю!", media_type="text/html")
    else:
        response = Response(f"Привет, {user['name']}!<br>Ваш баланс: {user['balance']}", 
                    media_type="text/html")
        username_signed = base64.b64encode(login.encode()).decode() + "." + sign_data(login)
        response.set_cookie(key="username", value=username_signed)
        return response
