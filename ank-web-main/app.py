# import Core modules
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
import pandas as pd 
import json

# import Store Enriched Data modules
from api import GetStoreById
from api import GetStoresIdsList
from api import GetStoreByFilter

# Sqlite & sqlalchemy specific modules
from sqlalchemy.orm import Session
from dbsetup.SqliteSetup import get_db, engine,get_bootstrap_ddl
from dbsetup.postgres import get_postgres_db
import sqlapp.Models as models
import sqlapp.ModelsPst as models_pst

import sqlapp.Schemas as schemas
from sqlapp.Repos import StoreRepo,ApplicationRepo, ViewRepo,ComponentRepo,FunctionRepo,UserRepo,ProductRepo, MasterRepo
from typing import List

#jwt authentication 
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

# function 
import random, string

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


# class User(BaseModel):
#     username: str
#     email: Union[str, None] = None
#     full_name: Union[str, None] = None
#     disabled: Union[bool, None] = None


# class UserInDB(User):
#     hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://20.232.153.176",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:6000",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str):
    user =UserRepo.get_user_by_username(db, userName=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    #user = get_user(fake_users_db, username=token_data.username)
    user = UserRepo.get_user_by_username(db=db,userName=token_data.username)
    
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@app.get("/bootstrap/db")
async def bootstrap_db(current_user: schemas.User = Depends(get_current_active_user),db: Session = Depends(get_db)):
    
    conn  = db.connection().connection
    conn.executescript (get_bootstrap_ddl())

    # db.execute("""
    # create table geeks_demo(
    #     geek_id,
    #     geek_name
    # );
    # """)

    return [{"item_id": "Foo", "owner": current_user.username}]

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: schemas.User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


# @app.get('/stores/{store_id}', tags=["Store Table Query"], response_model=schemas.Store)
# def get_stores(store_id: str, db: Session = Depends(get_db)):
#     """
#     Get the Store with the given store_id
#     """
#     store_db_entry = StoreRepo.get_store_by_store_id(db, store_id)
#     if store_db_entry is None:
#         raise HTTPException(status_code=404, detail="Store not found with the given storeId")
#     return store_db_entry


# @app.post('/stores', tags=["Stores table Query"], response_model=schemas.Store, status_code=201)
# async def create_store_entry(store_request: schemas.StoreCreate, db: Session = Depends(get_db)):
#     """
#     Create an new store entry and store it in the stores table
#     """
#     store_db_entry = StoreRepo.get_store_by_store_id(db, storeId=store_request.storeId)
#     if store_db_entry:
#         raise HTTPException(status_code=400, detail="Store with this storeId already exists!")

#     return await StoreRepo.create_new_entry(db=db, store=store_request)


@app.post('/application', tags=["Application Table Query"], response_model=schemas.Application, status_code=201)
async def create_application_entry(app_request: schemas.ApplicationCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    """
    Create an new application entry and store it in the application table
    """
    app_db_entry = ApplicationRepo.get_app_by_app_uuid(db, appUuid=app_request.app_uuid)
    if app_db_entry:
        raise HTTPException(status_code=400, detail="app with this uuid already exists!")

    return await ApplicationRepo.create_new_entry(db=db, application=app_request)

@app.get('/application/{app_uuid}', tags=["Application Table Query"])
def get_application(app_uuid: str, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    """
    Get the application with the given store_id
    """
    response = {}
    app_db_entry = ApplicationRepo.get_app_by_app_uuid(db, app_uuid)
    if app_db_entry is None:
        response['status'] = 'error'
        response['message'] = 'No application found with given id'
        raise response
    response['status']='success'
    response['data'] = app_db_entry
    return response

@app.put("/application/update", tags=["Application Table Query"]) #id is a path parameter
def update_application(app_request: schemas.ApplicationCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    
    app_db_entry = ApplicationRepo.get_app_by_app_uuid(db, app_request.app_uuid)
    response = {}
    if app_db_entry:
        updated_app = ApplicationRepo.update_application(db=db, application=app_request)
        response['status'] = 'success'
        response['message'] = 'Fetched Successfully'
        response['data'] = updated_app
        return updated_app
    else:
        response['status'] = 'error'
        response['message'] = f"Application with id {app_request.app_uuid} does not exist"
        return response

@app.delete("/application/delete/{app_uuid}/", tags=["Application Table Query"]) #id is a path parameter
def delete_application(app_uuid: str, db:Session=Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):

    app_db_entry = ApplicationRepo.get_app_by_app_uuid(db, app_uuid)
    #check if friend object exists
    response = {}
    if app_db_entry:

        ApplicationRepo.delete_application(db=db, appUuid=app_uuid)
        response['status'] = 'success'
        response['message'] = 'Deleted Successfully'
        return response
    else:
        response['status'] = 'error'
        response['message'] = f"Application with id {app_uuid} does not exist"
        return response


@app.get('/applicationList', tags=["Application Table Query"])
def get_all_application( db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    """
    Getting all the Application entries stored in the database
    """
    response = {}
    response['status'] = 'success'
    response['message'] = 'Fetched Successfully'
    response['data'] = ApplicationRepo.get_all_apps(db, user_id = current_user.username)
    return response


### Start of Views  #############

@app.post('/view', tags=["View Table Query"])
async def create_view_entry(view_request: schemas.ViewCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    
    app_view_entry = ViewRepo.get_view_by_view_uuid(db, viewUuid=view_request.view_uuid)
    response = {}
    if app_view_entry:
        response['status'] = 'error'
        response['status'] ='view with this uuid already exists!'
    else: 
        await ViewRepo.create_new_entry(db=db, view=view_request)
        response['status'] = 'success'
        response['status'] ='View Created Successfully !'

    return response

@app.get('/view/{view_uuid}', tags=["View Table Query"])
def get_view(view_uuid: str, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    response = {}
    view_db_entry = ViewRepo.get_view_by_view_uuid(db, view_uuid)
    if view_db_entry is None:
        response['status'] = 'error'
        response['message'] = 'No application found with given id'
        raise response
    response['status']='success'
    response['message']='View Fetchted Successfully'
    response['data'] = view_db_entry
    return response

@app.put("/view/update", tags=["View Table Query"]) #id is a path parameter
def update_application(view_request: schemas.ViewCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    
    view_db_entry = ViewRepo.get_view_by_view_uuid(db, view_request.view_uuid)
    response = {}
    if view_db_entry:
        updated_view = ViewRepo.update_view(db=db, view=view_request)
        response['status'] = 'success'
        response['message'] = 'Fetched Successfully'
        response['data'] = updated_view
        return updated_view
    else:
        response['status'] = 'error'
        response['message'] = f"View with id {view_request.view_uuid} does not exist"
        return response

@app.delete("/view/delete/{view_uuid}/", tags=["View Table Query"]) #id is a path parameter
def delete_view(view_uuid: str, db:Session=Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):

    view_db_entry = ViewRepo.get_view_by_view_uuid(db, viewUuid=view_uuid)
    #check if friend object exists
    response = {}
    if view_db_entry:

        ViewRepo.delete_view(db=db, viewUuid=view_uuid)
        response['status'] = 'success'
        response['message'] = 'Deleted Successfully'
        return response
    else:
        response['status'] = 'error'
        response['message'] = f"Application with id {app_uuid} does not exist"
        return response


@app.get('/viewList/{app_uuid}', tags=["View Table Query"])
def get_all_views(app_uuid: str, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    """
    Getting all the Application entries stored in the database
    """
    response = {}
    response['status'] = 'success'
    response['message'] = 'Fetched Successfully'
    response['data'] = ViewRepo.get_all_views(db=db, appUuid=app_uuid)
    return response

### End of Views ##############



### Start of Component  #############

@app.post('/component', tags=["Component Table Query"])
async def create_component_entry(component_request: schemas.ComponentCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    
    response = {}
    response['status'] = 'success'
    for component_item in component_request.components:
        component_view_entry = ComponentRepo.get_component_by_comp_uuid(db, compUuid=component_item.comp_uuid)

        if component_view_entry and component_item.is_add:
            response['status'] = 'error'
            response['status'] ='component with this uuid already exists!'

    if (response['status'] == 'success'):
        await ComponentRepo.create_new_entry(db=db, component=component_request)
        response['status'] = 'success'
        response['status'] ='Components Created/updated Successfully !'

    return response

    # component_view_entry = ComponentRepo.get_component_by_comp_uuid(db, compUuid=component_request.comp_uuid)
    # response = {}
    # if component_view_entry:
    #     response['status'] = 'error'
    #     response['status'] ='component with this uuid already exists!'
    # else: 
    #     await ComponentRepo.create_new_entry(db=db, component=component_request)
    #     response['status'] = 'success'
    #     response['status'] ='Component Created Successfully !'

    # return response

@app.get('/component/{component_uuid}', tags=["Component Table Query"])
def get_component(comp_uuid: str, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    response = {}
    component_db_entry = ComponentRepo.get_component_by_comp_uuid(db, comp_uuid)
    if component_db_entry is None:
        response['status'] = 'error'
        response['message'] = 'No component found with given id'
        raise response
    response['status']='success'
    response['message']='Component Fetchted Successfully'
    response['data'] = component_db_entry
    return response

@app.put("/component/update", tags=["Component Table Query"]) #id is a path parameter
def update_application(component_request: schemas.ComponentCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    
    component_db_entry = ComponentRepo.get_component_by_comp_uuid(db, component_request.comp_uuid)
    response = {}
    if component_db_entry:
        updated_component = ComponentRepo.update_component(db=db, component=component_request)
        response['status'] = 'success'
        response['message'] = 'Fetched Successfully'
        response['data'] = updated_component
        return updated_component
    else:
        response['status'] = 'error'
        response['message'] = f"Component with id {component_request.comp_uuid} does not exist"
        return response

@app.delete("/component/delete/{comp_uuid}/", tags=["Component Table Query"]) #id is a path parameter
def delete_component(comp_uuid: str, db:Session=Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):

    comp_db_entry = ComponentRepo.get_component_by_comp_uuid(db, compUuid=comp_uuid)
    #check if friend object exists
    response = {}
    if comp_db_entry:

        ComponentRepo.delete_component(db=db, compUuid=comp_uuid)
        response['status'] = 'success'
        response['message'] = 'Deleted Successfully'
        return response
    else:
        response['status'] = 'error'
        response['message'] = f"component with id {comp_uuid} does not exist"
        return response


@app.get('/compList/{view_uuid}', tags=["Component Table Query"])
def get_all_components(view_uuid: str, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    """
    Getting all the Application entries stored in the database
    """
    response = {}
    response['status'] = 'success'
    response['message'] = 'Fetched Successfully'
    response['data'] = ComponentRepo.get_all_component(db=db, viewUuid=view_uuid)
    return response

### End of Views ##############



### Start of Property  #############

# @app.post('/property', tags=["Property Table Query"])
# async def create_property_entry(property_request: schemas.PropertyCreate, db: Session = Depends(get_db)):
#     print (property_request)
#     response = {}
#     response['status'] = 'success'
#     for property in property_request.properties:
#         property_comp_entry = PropertyRepo.get_property_by_prp_uuid(db, propUuid=property.prop_uuid)

#         if property_comp_entry:
#             response['status'] = 'error'
#             response['status'] ='property with this uuid already exists!'

#     if (response['status'] == 'success'):
#         await PropertyRepo.create_new_entry(db=db, properties=property_request)
#         response['status'] = 'success'
#         response['status'] ='Properties Created Successfully !'

#     return response

# @app.get('/property/{property_uuid}', tags=["Property Table Query"])
# def get_property(prop_uuid: str, db: Session = Depends(get_db)):
#     response = {}
#     property_comp_entry = PropertyRepo.get_property_by_prp_uuid(db, propUuid=prop_uuid)
#     if property_comp_entry is None:
#         response['status'] = 'error'
#         response['message'] = 'No property found with given id'
#         raise response
#     response['status']='success'
#     response['message']='Component Fetchted Successfully'
#     response['data'] = property_comp_entry
#     return response

# @app.put("/property/update", tags=["Property Table Query"]) #id is a path parameter
# def update_property(property_request: schemas.PropertyCreate, db: Session = Depends(get_db)):
    
#     response = {}
#     PropertyRepo.update_properties(db, property_request)
#     response['status'] = 'success'
#     response['message'] = 'Updated Successfully'
#     return response

# @app.delete("/property/delete/{prop_uuid}/", tags=["Property Table Query"]) #id is a path parameter
# def delete_property(prop_uuid: str, db:Session=Depends(get_db)):

    
#     property_comp_entry = PropertyRepo.get_property_by_prp_uuid(db, propUuid=prop_uuid)
#     #check if friend object exists
#     response = {}
#     if property_comp_entry:

#         PropertyRepo.delete_property(db=db, propUuid=prop_uuid)
#         response['status'] = 'success'
#         response['message'] = 'Deleted Successfully'
#         return response
#     else:
#         response['status'] = 'error'
#         response['message'] = f"property with id {prop_uuid} does not exist"
#         return response


# @app.get('/propList/{comp_uuid}', tags=["Property Table Query"])
# def get_all_components(comp_uuid: str, db: Session = Depends(get_db)):
#     """
#     Getting all the Application entries stored in the database
#     """
#     response = {}
#     response['status'] = 'success'
#     response['message'] = 'Fetched Successfully'
#     response['data'] = PropertyRepo.get_all_properties(db,compUuid= comp_uuid)
#     return response

## End of Views ##############




### Start of Function  #############

@app.post('/function', tags=["Function Table Query"])
async def create_function_entry(function_request: schemas.FunctionCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    
    function_entry = FunctionRepo.get_function_by_function_uuid(db, funcUuid=function_request.func_uuid)
    response = {}
    if function_entry:
        response['status'] = 'error'
        response['status'] ='Function with this uuid already exists!'
    else: 
        await FunctionRepo.create_new_entry(db=db, function=function_request)
        response['status'] = 'success'
        response['status'] ='Function Created Successfully !'
    return response

@app.get('/function/{function_uuid}', tags=["Function Table Query"])
def get_function(function_uuid: str, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    response = {}
    function_db_entry = FunctionRepo.get_function_by_function_uuid(db, funcUuid=function_uuid)
    if function_db_entry is None:
        response['status'] = 'error'
        response['message'] = 'No Function found with given id'
        raise response
    response['status']='success'
    response['message']='Function Fetchted Successfully'
    response['data'] = function_db_entry
    return response

@app.put("/function/update", tags=["Function Table Query"]) #id is a path parameter
def update_function(function_request: schemas.FunctionCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    
    function_db_entry = FunctionRepo.get_function_by_function_uuid(db, funcUuid=function_request.func_uuid)
    response = {}
    if function_db_entry:
        updated_function = FunctionRepo.update_component(db=db, function=function_request)
        response['status'] = 'success'
        response['message'] = 'Fetched Successfully'
        response['data'] = updated_function
        return response
    else:
        response['status'] = 'error'
        response['message'] = f"functionwith id {function_request.func_uuid} does not exist"
        return response

@app.delete("/function/delete/{function_uuid}/", tags=["Function Table Query"]) #id is a path parameter
def delete_function(function_uuid: str, db:Session=Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):

    func_db_entry = FunctionRepo.get_function_by_function_uuid(db, funcUuid=function_uuid)
    #check if friend object exists
    response = {}
    if func_db_entry:

        FunctionRepo.delete_function(db=db, funcUuid=function_uuid)
        response['status'] = 'success'
        response['message'] = 'Deleted Successfully'
        return response
    else:
        response['status'] = 'error'
        response['message'] = f"function with id {function_uuid} does not exist"
        return response


@app.get('/functionList/', tags=["Function Table Query"])
def get_all_functions(db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    """
    Getting all the Application entries stored in the database
    """
    response = {}
    response['status'] = 'success'
    response['message'] = 'Fetched Successfully'
    response['data'] = FunctionRepo.get_all_function(db=db)
    return response

### End of Function ##############


# Home/Index Page GET method, return HTML
@app.get('/', response_class=HTMLResponse)
@app.get('/home', response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Home connect"})


# Service hello api, GET method, return string
@app.get("/hello", response_class=PlainTextResponse)
async def hello():
    return "Hello Scribble World!!"


# # Please make a call as below from command prompt
# # curl --request GET http://127.0.0.1:8000/getStoresIds
# # -----
# @app.get("/getStoresIds", tags=["Stores Enriched Data Query"],  response_class=JSONResponse)
# async def get_store_ids():
#     return GetStoresIdsList.generate_query_response()


# # Please make a call as below from command prompt
# # curl --request POST -H 'Content-Type: application/json' \
# #   -d '{"storeId":"432"}' \
# #   http://127.0.0.1:8000/getStoreById
# # -----
# @app.post("/getStoreById", tags=["Stores Enriched Data Query"], response_class=JSONResponse)
# async def get_store(query: GetStoreById.Query):
#     return GetStoreById.generate_query_response(query)


# # Please make a call as below from command prompt
# # curl --request POST -H 'Content-Type: application/json' \
# #  -d '{"filterName":"state", "filterValue": "ca", "filterCondition": "==", "limitResult": 10}' \
# #  http://127.0.0.1:8000/getStoreByFilter
# # -----
# @app.post("/getStoreByFilter", tags=["Stores Enriched Data Query"], response_class=JSONResponse)
# async def get_store(query: GetStoreByFilter.Query):
#     return GetStoreByFilter.generate_query_response(query)


# Database Connection api, GET method, return string
@app.get('/dbStatus', tags=["DB Status"], response_class=PlainTextResponse)
async def get_database_status(db: Session = Depends(get_db)):
    if db.is_active:
        return 'Database is connected..'
    return 'Database is not connected..'

# Database Connection api, GET method, return string
@app.get('/postgres', tags=["DB Status"], response_class=PlainTextResponse)
async def get_database_status(db: Session = Depends(get_postgres_db)):
    if db.is_active:
        return 'Database is connected..'
    return 'Database is not connected..'

@app.post('/function_execute/', tags=["Function Table Query"])
async def func_execute(function_request: schemas.FunctionCreate, db: Session = Depends(get_postgres_db),current_user: schemas.User = Depends(get_current_active_user)):

    response = {}
    input_param = json.loads( function_request.input_param)
    if function_request.key_name == 'GetProductsByDept':
        response['product_list'] = jsonable_encoder(ProductRepo.get_all_productsb_by_dept(db=db,dep_id =str(input_param[0]['dept_id'])))
        response['status'] = 'success'
        response['message'] = 'Fetched Successfully'
    elif function_request.key_name == 'GetProductsByAisle':
        response['product_list'] = jsonable_encoder(ProductRepo.get_all_productsb_by_aisle(db=db,aisle_id =str(input_param[0]['aisle_id'])))
        response['status'] = 'success'
        response['message'] = 'Fetched Successfully'
    elif function_request.key_name == 'GetDepartmentList':
        response['department_list'] = jsonable_encoder(MasterRepo.get_all_departments(db=db))
        response['status'] = 'success'
        response['message'] = 'Fetched Successfully'
    elif function_request.key_name == 'GetAisleList':
        response['aisle_list'] = jsonable_encoder(MasterRepo.get_all_aisle(db=db))
        response['status'] = 'success'
        response['message'] = 'Fetched Successfully'
    elif function_request.key_name == 'GetHeader':
        WORDS = ("Introduction", "Overview", "Section", "Topic", "Title",  "Summary")
        response['header_text'] =random.choice(WORDS)
        response['status'] = 'success'
        response['message'] = 'Fetched Successfully'
    elif function_request.key_name == 'GetImageUrl':
        ImageUrlList = { "image_1" : "http://www.imagesource.com/image1.gif",
        "image_2" : "http://www.imagesource.com/image2.gif",
        "image_3" : "http://www.imagesource.com/image3.gif",
        "image_4" : "http://www.imagesource.com/image4.gif", 
        "image_5" : "http://www.imagesource.com/image5.gif"
         }
        response['header_text'] =ImageUrlList[input_param[0]['image_num']]
        response['status'] = 'success'
        response['message'] = 'Fetched Successfully'
    else:
        response['status'] = 'error'
        response['message'] = 'Invalid Function Definition'

    return response

# Main App as app.py
# How to Run from command line
#          $ uvicorn app:app --reload
if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000)