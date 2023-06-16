from fastapi import FastAPI
from fastapi.responses import Response


app = FastAPI() # экземпляр приложения fastapi

@app.get("/")
def index_page():
    """Индексная страничка приложения"""
    with open("./templates/login.html", "r") as f:
        login_page = f.read()
    return Response(login_page, media_type="text/html") # media_type устанавливает http заголовок content_type (utf-8 по умолчанию) 
