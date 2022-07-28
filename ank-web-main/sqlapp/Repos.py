from email.mime import application
from sqlalchemy.orm import Session
import random, string
from . import Models, Schemas, ModelsPst
from datetime import datetime

# Main Store Repository
class StoreRepo:
    # This method saves the store entry data sent from API
    async def create_new_entry(db: Session, store: Schemas.StoreCreate):
        store_db_entry = Models.Store(storeId=store.storeId,
                                     city=store.city,
                                     state=store.state,
                                     zipCode=store.zipCode,
                                     latitude=store.latitude,
                                     longitude=store.longitude)
        db.add(store_db_entry)
        db.commit()
        db.refresh(store_db_entry)
        return store_db_entry

    # This method returns a single store from the sqlite database, by passing the storeId from API
    def get_store_by_store_id(db: Session, storeId):
        return db.query(Models.Store).filter(Models.Store.storeId == storeId).first()

    # This method returns a list of all stored stores in the sqllite database
    def get_all_stores(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Models.Store).offset(skip).limit(limit).all()

class ApplicationRepo:
    # This method saves the store entry data sent from API
    async def create_new_entry(db: Session, application: Schemas.ApplicationCreate):
        app_db_entry = Models.Application(app_uuid=application.app_uuid,
                                     app_name=application.app_name, session_id =application.session_id, 
                                     user_uid = application.user_uid) 
        

        db.add(app_db_entry)
        db.commit()
        db.refresh(app_db_entry)
        return app_db_entry

    # This method returns a single store from the sqlite database, by passing the storeId from API
    def get_app_by_app_uuid(db: Session, appUuid):
        return db.query(Models.Application).filter(Models.Application.app_uuid == appUuid).first()

    def update_application(db:Session, application: Schemas.ApplicationCreate):
        """
        Update a Application object's attributes
        """
        db_app = ApplicationRepo.get_app_by_app_uuid(db=db, appUuid=application.app_uuid)
        db_app.app_name = application.app_name

        db.commit()
        db.refresh(db_app) #refresh the attribute of the given instance
        return db_app



    # This method returns a list of all stored stores in the sqllite database
    def get_all_apps(db: Session, user_id, skip: int = 0, limit: int = 100):
        return db.query(Models.Application).filter(Models.Application.user_uid == user_id).offset(skip).limit(limit).all()


    def delete_application(db:Session, appUuid):
        """
        Delete a Application object
        """
        db_app = ApplicationRepo.get_app_by_app_uuid(db=db, appUuid=appUuid)
        db.delete(db_app)
        db.commit() #save changes to db



class ViewRepo:
    # This method saves the store entry data sent from API
    async def create_new_entry(db: Session, view: Schemas.ViewCreate):
        view_db_entry = Models.View(view_uuid= view.view_uuid, app_uuid=view.app_uuid,
                                     view_name=view.view_name, user_uid = view.user_uid, session_id =view.session_id )
        view_db_entry.preview_id =   ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
                           
        db.add(view_db_entry)
        db.commit()
        db.refresh(view_db_entry)
        return view_db_entry

    # This method returns a single store from the sqlite database, by passing the storeId from API
    def get_view_by_view_uuid(db: Session, viewUuid):
        return db.query(Models.View).filter(Models.View.view_uuid == viewUuid).first()

    def update_view(db:Session, view: Schemas.ViewCreate):
        
        db_view = ViewRepo.get_view_by_view_uuid(db=db, viewUuid=view.view_uuid)
        db_view.view_name = view.view_name

        db.commit()
        db.refresh(db_view) #refresh the attribute of the given instance
        return db_view


    # This method returns a list of all stored stores in the sqllite database
    def get_all_views(db: Session, appUuid, skip: int = 0, limit: int = 100):
        return db.query(Models.View).filter(Models.View.app_uuid == appUuid).offset(skip).limit(limit).all()


    def delete_view(db:Session, viewUuid):
        db_view = ViewRepo.get_view_by_view_uuid(db=db, viewUuid=viewUuid)
        db.delete(db_view)
        db.commit() #save changes to db



class ComponentRepo:
    # This method saves the store entry data sent from API
    async def create_new_entry(db: Session, component: Schemas.ComponentCreate):

        for component_item in component.components:

            if component_item.is_add:
                db_component = Models.Component(comp_uuid=component_item.comp_uuid, view_uuid= component.view_uuid, app_uuid=component.app_uuid,
                                            comp_name=component_item.comp_name,meta_data=component_item.meta_data,
                                            properties=component_item.properties,
                                            user_uid = component.user_uid,  session_id =component.session_id)
                db.add(db_component)
                
            else:
                db_component = ComponentRepo.get_component_by_comp_uuid(db=db, compUuid=component_item.comp_uuid)
                db_component.comp_name = component_item.comp_name
                db_component.meta_data = component_item.meta_data
                db_component.properties = component_item.properties

            db.commit()
            db.refresh(db_component)

        return db_component

    # This method returns a single store from the sqlite database, by passing the storeId from API
    def get_component_by_comp_uuid(db: Session, compUuid):
        return db.query(Models.Component).filter(Models.Component.comp_uuid == compUuid).first()

    def update_component(db:Session, component: Schemas.ComponentCreate):
        
        db_component = ComponentRepo.get_component_by_comp_uuid(db=db, compUuid=component.comp_uuid)
        db_component.comp_name = component.comp_name
        db_component.meta_data = component.meta_data
        db_component.properties = component.properties

        db.commit()
        db.refresh(db_component) #refresh the attribute of the given instance
        return db_component


    # This method returns a list of all stored stores in the sqllite database
    def get_all_component(db: Session, viewUuid, skip: int = 0, limit: int = 100):
        return db.query(Models.Component).filter(Models.Component.view_uuid == viewUuid).offset(skip).limit(limit).all()


    def delete_component(db:Session, compUuid):
        db_component = ComponentRepo.get_component_by_comp_uuid(db=db, compUuid=compUuid)
        db.delete(db_component)
        db.commit() #save changes to db

# class PropertyRepo:
#     # This method saves the store entry data sent from API
#     async def create_new_entry(db: Session, properties: Schemas.PropertyCreate):

#         for property in properties.properties:
#             property_db_entry = Models.Property(comp_uuid=properties.comp_uuid, 
#                                 view_uuid= properties.view_uuid, app_uuid=properties.app_uuid,
#                                         prop_uuid=property.prop_uuid,
#                                         prop_name=property.prop_name,prop_type=property.prop_type,
#                                         prop_value=property.prop_value, user_id = properties.user_id,  
#                                         session_id =properties.session_id)
#             db.add(property_db_entry)
#             db.commit()
#             db.refresh(property_db_entry)

#         return property_db_entry

#     # This method returns a single store from the sqlite database, by passing the storeId from API
#     def get_property_by_prp_uuid(db: Session, propUuid):
#         return db.query(Models.Property).filter(Models.Property.prop_uuid == propUuid).first()

#     def update_properties(db:Session, propertyCreate: Schemas.PropertyCreate):
#         db_property={}
#         for property in propertyCreate.properties:
            
#             db_property = PropertyRepo.get_property_by_prp_uuid(db=db, propUuid=property.prop_uuid)
#             print (db_property)
#             db_property.prop_name = property.prop_name
#             db_property.prop_value = property.prop_value
#             db_property.prop_type = property.prop_type
#             db.commit()
#             db.refresh(db_property) #refresh the attribute of the given instance

#         return db_property
        


#     # This method returns a list of all stored stores in the sqllite database
#     def get_all_properties(db: Session, compUuid, skip: int = 0, limit: int = 100):
#         return db.query(Models.Property).filter(Models.Property.comp_uuid == compUuid).offset(skip).limit(limit).all()


#     def delete_property(db:Session, propUuid):
#         db_property = PropertyRepo.get_property_by_prp_uuid(db=db, propUuid=propUuid)
#         db.delete(db_property)
#         db.commit() #save changes to db

class FunctionRepo:
    # This method saves the store entry data sent from API
    async def create_new_entry(db: Session, function: Schemas.FunctionCreate):
        function_db_entry = Models.Function(func_uuid=function.func_uuid, key_name=function.key_name, desc= function.desc, input_param=function.input_param,
                                     output_param=function.output_param)
        db.add(function_db_entry)
        db.commit()
        db.refresh(function_db_entry)
        return function_db_entry

    # This method returns a single store from the sqlite database, by passing the storeId from API
    def get_function_by_function_uuid(db: Session, funcUuid):
        return db.query(Models.Function).filter(Models.Function.func_uuid == funcUuid).first()

    def update_component(db:Session, function: Schemas.FunctionBase):
        
        db_function = FunctionRepo.get_function_by_function_uuid(db=db, funcUuid=function.func_uuid)
        db_function.key_name = function.key_name
        db_function.desc = function.desc
        db_function.input_param = function.input_param
        db_function.output_param = function.output_param

        db.commit()
        db.refresh(db_function) #refresh the attribute of the given instance
        return db_function


    # This method returns a list of all stored stores in the sqllite database
    def get_all_function(db: Session,  skip: int = 0, limit: int = 100):
        return db.query(Models.Function).offset(skip).limit(limit).all()


    def delete_function(db:Session, funcUuid):
        db_function = FunctionRepo.get_function_by_function_uuid(db=db, funcUuid=funcUuid)
        db.delete(db_function)
        db.commit() #save changes to db


class UserRepo:
    # This method saves the store entry data sent from API
    async def create_new_entry(db: Session, user: Schemas.UserCreate):
        user_db_entry = Models.User(username=user.username, full_name=user.full_name, 
                                email= user.email)
        db.add(user_db_entry)
        db.commit()
        db.refresh(user_db_entry)
        return user_db_entry

    # This method returns a single store from the sqlite database, by passing the storeId from API
    def get_user_by_username(db: Session, userName):
        return db.query(Models.User).filter(Models.User.username == userName).first()


class ProductRepo:
    # This method saves the store entry data sent from API
    def get_all_productsb_by_dept(db: Session, dep_id:str, skip: int = 0, limit: int = 100):
        return db.query(ModelsPst.Product).filter(ModelsPst.Product.department_id == dep_id).offset(skip).limit(limit).all()
    def get_all_productsb_by_aisle(db: Session, aisle_id:str, skip: int = 0, limit: int = 100):
        return db.query(ModelsPst.Product).filter(ModelsPst.Product.aisle_id == aisle_id).offset(skip).limit(limit).all()

class MasterRepo:
    def get_all_departments(db: Session, skip: int = 0, limit: int = 100):
        return db.query(ModelsPst.Department).offset(skip).limit(limit).all()
    def get_all_aisle(db: Session, skip: int = 0, limit: int = 100):
        return db.query(ModelsPst.Aisle).offset(skip).limit(limit).all()


