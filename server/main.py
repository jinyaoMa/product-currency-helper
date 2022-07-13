import re
from app_singleton import App
from services_facade import ProductCurrencyHelperServices
from typing import Union
from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

services = ProductCurrencyHelperServices()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=App().admin_token)

IS_LOGIN = "islogin"
PERMISSION = "permission"


class ProductForm(BaseModel):
    id: Union[int, None] = None
    title: str
    url: str
    img: str
    price: float
    base: str


@app.get("/access/{access_token}")
def access_with_token(request: Request, access_token: str):
    request.session[PERMISSION] = services.check_token(access_token)
    if request.session[PERMISSION] == "":
        request.session[IS_LOGIN] = False
    else:
        request.session[IS_LOGIN] = True
    return request.session[PERMISSION]


@app.get("/base-options")
def get_base_options(request: Request):
    if request.session[IS_LOGIN] and len(re.findall("basic:1", request.session[PERMISSION])) > 0:
        base_options = services.get_base_options()
        return {
            "data": base_options
        }
    return {"error": "logout"}


@app.get("/api/{which}/base/{base}")
def get_rate_dict(request: Request, which: str, base: str):
    if request.session[IS_LOGIN] and len(re.findall("basic:1", request.session[PERMISSION])) > 0:
        base_options = services.get_rate_dict(which, base)
        return {
            "data": base_options
        }
    return {"error": "logout"}


@app.get("/token/list")
def get_token_list(request: Request):
    if request.session[IS_LOGIN] and len(re.findall("advanced:1", request.session[PERMISSION])) > 0:
        token_list = services.get_token_list()
        return {
            "data": token_list
        }
    return {"error": "logout"}


@app.put("/token/{permission_string}")
def create_token(request: Request, permission_string: str):
    if request.session[IS_LOGIN] and len(re.findall("advanced:1", request.session[PERMISSION])) > 0:
        token = services.create_token(permission_string)
        return {
            "id": token.id,
            "token": token.access_token,
            "permission": token.permission,
            "active": token.active
        }
    return {"error": "logout"}


@app.post("/token/{id}/deactivate")
def deactivate_token(request: Request, id: int):
    if request.session[IS_LOGIN] and len(re.findall("advanced:1", request.session[PERMISSION])) > 0:
        services.deactivate_token(id)
        return {
            "success": True,
        }
    return {"error": "logout"}


@app.post("/token/{id}/activate")
def activate_token(request: Request, id: int):
    if request.session[IS_LOGIN] and len(re.findall("advanced:1", request.session[PERMISSION])) > 0:
        services.activate_token(id)
        return {
            "success": True,
        }
    return {"error": "logout"}


@app.get("/product/list")
def get_product_list(request: Request):
    if request.session[IS_LOGIN] and len(re.findall("basic:1", request.session[PERMISSION])) > 0:
        product_list = services.get_product_list()
        return {
            "data": product_list
        }
    return {"error": "logout"}


@app.put("/product")
def create_product(request: Request, product_form: ProductForm):
    if request.session[IS_LOGIN] and len(re.findall("manipulation:1", request.session[PERMISSION])) > 0:
        product = services.create_product({
            "title": product_form.title,
            "url": product_form.url,
            "img": product_form.img,
            "price": product_form.price,
            "base": product_form.base,
        })
        return {
            "id": product.id,
            "title": product.title,
            "url": product.url,
            "img": product.img,
            "price": product.price,
            "base": product.base
        }
    return {"error": "logout"}


@app.post("/product")
def update_product(request: Request, product_form: ProductForm):
    if request.session[IS_LOGIN] and len(re.findall("manipulation:1", request.session[PERMISSION])) > 0:
        product = services.update_product({
            "id": product_form.id,
            "title": product_form.title,
            "url": product_form.url,
            "img": product_form.img,
            "price": product_form.price,
            "base": product_form.base,
        })
        return {
            "id": product.id,
            "title": product.title,
            "url": product.url,
            "img": product.img,
            "price": product.price,
            "base": product.base
        }
    return {"error": "logout"}


@app.delete("/product/{id}")
def delete_product(request: Request, id: int):
    if request.session[IS_LOGIN] and len(re.findall("manipulation:1", request.session[PERMISSION])) > 0:
        services.delete_product(id)
        return {
            "success": True,
        }
    return {"error": "logout"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=App().server_port)
