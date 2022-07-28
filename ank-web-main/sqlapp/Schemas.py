from typing import List, Optional
from pydantic import BaseModel, create_model


# Main Store Table Schema with main fields
class StoreBase(BaseModel):
    storeId: str
    city: str
    state: str
    zipCode: int
    latitude: float
    longitude: float
    # storeName: Optional[str] = None


# This class is used when we create a new store record by passing the main fields data
class StoreCreate(StoreBase):
    pass

# Master Store Class
class Store(StoreBase):
    id: int

    class Config:
        orm_mode = True

# Main Store Table Schema with main fields
class ApplicationBase(BaseModel):
    app_uuid: str
    app_name: str
    session_id: str
    user_uid: str

    # storeName: Optional[str] = None


# This class is used when we create a new store record by passing the main fields data
class ApplicationCreate(ApplicationBase):
    pass



# Master Store Class
class Application(ApplicationBase):
    id: int

    class Config:
        orm_mode = True



class ViewBase(BaseModel):
    app_uuid: str
    view_uuid: str
    view_name: str
    session_id: str
    user_uid: str


class ViewCreate(ViewBase):
    pass


# Master Store Class
class View(ViewBase):
    id: int

    class Config:
        orm_mode = True

class ComponentBase(BaseModel):
    app_uuid: str
    view_uuid: str
    components: List[create_model('components', comp_name=(str, ...), meta_data=(str, ...),
    properties=(str, ...), comp_uuid=(str, ...), is_add=(bool,...))] = None
    # comp_uuid: str
    # comp_name: str
    # meta_data: str
    # properties: str
    session_id: str
    user_uid: str

class ComponentCreate(ComponentBase):
    pass


# Master Store Class
class Component(ComponentBase):
    id: int

    class Config:
        orm_mode = True



class PropertyBase(BaseModel):
    properties: List[create_model('properties', prop_name=(str, ...), prop_type=(str, ...),
    prop_value=(str, ...), prop_uuid=(str, ...))] = None
    
    app_uuid: str
    view_uuid: str
    comp_uuid: str
    # prop_uuid: str
    # prop_name: str
    # prop_type: str
    # prop_value: str
    session_id: str
    user_id: str

class PropertyCreate(PropertyBase):
    pass


# Master Store Class
class Property(ComponentBase):
    id: int

    class Config:
        orm_mode = True

class FunctionBase(BaseModel):
    func_uuid:str
    key_name: str
    desc: str
    input_param: str
    output_param: str


class FunctionCreate(FunctionBase):
    pass


# Master Store Class
class Function(FunctionBase):
    id: int

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    disabled: bool

    class Config:
        orm_mode = True

class UserCreate(User):
    pass
