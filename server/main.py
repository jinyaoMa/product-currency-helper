################################################################################
# API server
#
# Purpose: Expose services with access control to the front via FastAPI
#          and Uvicorn http server.
#
# Reference:
# FastAPI https://fastapi.tiangolo.com/
# Uvicorn https://www.uvicorn.org/#uvicornrun
#
# Student Name: Jinyao Ma
# Student ID:   001433428
#
################################################################################

from app_singleton import App
from services_facade import ProductCurrencyHelperServices
from typing import Union
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import re

# Initialize server and service layer
app = FastAPI()
services = ProductCurrencyHelperServices()

# Enable CORS to allow enter from front end - localhost port 8080
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Enable cookie-based session
IS_LOGIN = "islogin"
PERMISSION = "permission"
app.add_middleware(
    SessionMiddleware,
    secret_key=App().admin_token,
    session_cookie="PCH_KEY",
    max_age=10*24*60*60  # 10 days, in seconds
)


class ProductForm(BaseModel):
    # Structure of input from http request to add/update a product
    id: Union[int, None] = None  # no id needed for adding a product
    title: str
    url: str
    img: str
    price: float
    base: str


# User login with access token
@app.get("/api/access/{access_token}", status_code=status.HTTP_200_OK)
def access_with_token(request: Request, response: Response, access_token: str):
    request.session[PERMISSION] = services.check_token(access_token)
    if request.session[PERMISSION] == "":
        request.session[IS_LOGIN] = False
        return {"error": "invalid access token"}
    request.session[IS_LOGIN] = True
    response.set_cookie(
        "PCH_PERM",
        request.session[PERMISSION],
        10*24*60*60  # 10 days, in seconds
    )
    return {
        "success": True
    }


# User logout if it is currently logged in
@app.get("/api/logout", status_code=status.HTTP_200_OK)
def logout(request: Request, response: Response):
    if request.session[IS_LOGIN]:
        request.session[IS_LOGIN] = False
        response.set_cookie("PCH_PERM", "")
        return {
            "success": True
        }
    else:
        return {"error": "logout"}


# Get currency base options, available for users with basic permission
@app.get("/api/base-options", status_code=status.HTTP_200_OK)
def get_base_options(request: Request):
    if request.session[IS_LOGIN] and len(re.findall("basic:1", request.session[PERMISSION])) > 0:
        base_options = services.get_base_options()
        return {
            "success": True,
            "data": base_options
        }
    return {"error": "logout"}


# Get web service options, available for users with basic permission
@app.get("/api/api-options", status_code=status.HTTP_200_OK)
def get_api_options(request: Request):
    if request.session[IS_LOGIN] and len(re.findall("basic:1", request.session[PERMISSION])) > 0:
        api_options = services.get_api_options()
        return {
            "success": True,
            "data": api_options
        }
    return {"error": "logout"}


# Get exchange rate list, available for users with basic permission
@app.get("/api/service/{which}/base/{base}", status_code=status.HTTP_200_OK)
def get_rate_dict(request: Request, which: str, base: str):
    if request.session[IS_LOGIN] and len(re.findall("basic:1", request.session[PERMISSION])) > 0:
        rate_dict = services.get_rate_dict(which, base)
        return {
            "success": True,
            "data": rate_dict
        }
    return {"error": "logout"}


# Get token list, available for users with advanced permission
@app.get("/api/token/list", status_code=status.HTTP_200_OK)
def get_token_list(request: Request):
    if request.session[IS_LOGIN] and len(re.findall("advanced:1", request.session[PERMISSION])) > 0:
        token_list = services.get_token_list()
        return {
            "success": True,
            "data": token_list
        }
    return {"error": "logout"}


# Create a new token, available for users with advanced permission
@app.put("/api/token/{permission_string}", status_code=status.HTTP_200_OK)
def create_token(request: Request, permission_string: str):
    if request.session[IS_LOGIN] and len(re.findall("advanced:1", request.session[PERMISSION])) > 0:
        token = services.create_token(permission_string)
        return {
            "success": True,
            "data": token.data
        }
    return {"error": "logout"}


# Deactivate a token, available for users with advanced permission
@app.post("/api/token/{id}/deactivate", status_code=status.HTTP_200_OK)
def deactivate_token(request: Request, id: int):
    if request.session[IS_LOGIN] and len(re.findall("advanced:1", request.session[PERMISSION])) > 0:
        services.deactivate_token(id)
        return {
            "success": True,
        }
    return {"error": "logout"}


# Re-activate a token, available for users with advanced permission
@app.post("/api/token/{id}/activate", status_code=status.HTTP_200_OK)
def activate_token(request: Request, id: int):
    if request.session[IS_LOGIN] and len(re.findall("advanced:1", request.session[PERMISSION])) > 0:
        services.activate_token(id)
        return {
            "success": True,
        }
    return {"error": "logout"}


# Get product list, available for users with basic permission
@app.get("/api/product/list", status_code=status.HTTP_200_OK)
def get_product_list(request: Request):
    if request.session[IS_LOGIN] and len(re.findall("basic:1", request.session[PERMISSION])) > 0:
        product_list = services.get_product_list()
        return {
            "success": True,
            "data": product_list
        }
    return {"error": "logout"}


# Create a new product, available for users with manipulation permission
@app.put("/api/product", status_code=status.HTTP_200_OK)
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
            "success": True,
            "data": product.data
        }
    return {"error": "logout"}


# Update a product, available for users with manipulation permission
@app.post("/api/product", status_code=status.HTTP_200_OK)
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
            "success": True,
            "data": product.data
        }
    return {"error": "logout"}


# Delete a product, available for users with manipulation permission
@app.delete("/api/product/{id}", status_code=status.HTTP_200_OK)
def delete_product(request: Request, id: int):
    if request.session[IS_LOGIN] and len(re.findall("manipulation:1", request.session[PERMISSION])) > 0:
        services.deactivate_product(id)
        return {
            "success": True,
        }
    return {"error": "logout"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=App().server_port)
