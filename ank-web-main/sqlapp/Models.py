from sqlalchemy import BigInteger, Column, Integer, String, Float, ForeignKey,DateTime,Boolean
from dbsetup.SqliteSetup import Base
from sqlalchemy.sql import func

import datetime
# class Store(Base):
#     __tablename__ = "stores"

#     id = Column(Integer, primary_key=True, index=True)
#     storeId = Column(String(80), nullable=False, unique=True, index=True)
#     city = Column(String(200), nullable=False)
#     state = Column(String(200), nullable=False)
#     zipCode = Column(Integer, nullable=False)
#     latitude = Column(Float(precision=6), nullable=False)
#     longitude = Column(Float(precision=6), nullable=False)

#     def __repr__(self):
#         return 'StoreModel(storeId=%s, state=%s, city=%s, zipCode=%s, latitude=%s, longitude=%s)' % \
#                (self.storeId, self.views, self.likes, self.dislikes, self.latitude, self.longitude)

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    app_uuid = Column(String(80), nullable=False, unique=True, index=True)
    app_name = Column(String(200), nullable=False)

    user_uid = Column(BigInteger, nullable=False,  index=True)
    session_id = Column(String(200), nullable=False,  index=True)
    created_datetime =Column(DateTime, nullable=False,  index=True,  default=func.now())
    updated_datetime =Column(DateTime, nullable=False,  index=True, default=func.now())
    updated_by =Column(String(80), nullable=False, unique=True, index=True)
    
    

    def __repr__(self):
        return 'AppModel(app_id=%s, app_uuid=%s, app_name=%s)' % \
               (self.id, self.app_uuid, self.app_name)

class View(Base):
    __tablename__ = "views"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    view_uuid = Column(String(80), nullable=False, unique=True, index=True)
    app_uuid = Column(String(80), ForeignKey("applications.app_uuid"), nullable=False, unique=True, index=True)
    view_name = Column(String(200), nullable=False)
    preview_id = Column(String(50), nullable=False)
    user_uid = Column(BigInteger, nullable=False,  index=True)
    session_id = Column(String(200), nullable=False,  index=True)
    created_datetime =Column(DateTime, nullable=False,  index=True,  default=func.now())
    updated_datetime =Column(DateTime, nullable=False,  index=True, default=func.now())
    updated_by =Column(String(80), nullable=False, unique=True, index=True)

    def __repr__(self):
        return 'ViewModel(view_id=%s, view_uuid=%s, app_uuid=%s, view_name=%s)' % \
               (self.id, self.view_uuid, self.app_uuid, self.view_name)

class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comp_uuid = Column(String(80), nullable=False, unique=True, index=True)
    view_uuid = Column(String(80),ForeignKey("views.view_uuid"), nullable=False, unique=True, index=True)
    app_uuid = Column(String(80), ForeignKey("applications.app_uuid"), nullable=False, unique=True, index=True)
    comp_name = Column(String(200), nullable=False)
    meta_data = Column(String(400), nullable=False)
    properties = Column(String(500), nullable=False)
    user_uid = Column(BigInteger, nullable=False,  index=True)
    session_id = Column(String(200), nullable=False,  index=True)
    created_datetime =Column(DateTime, nullable=False,  index=True,  default=func.now())
    updated_datetime =Column(DateTime, nullable=False,  index=True, default=func.now())
    updated_by =Column(String(80), nullable=False, unique=True, index=True)

    def __repr__(self):
        return 'CompModel(comp_id=%s, comp_uuid=%s,  view_uuid=%s, app_uuid=%s, comp_name=%s)' % \
               (self.id, self.comp_uuid, self.view_uuid, self.app_uuid, self.comp_name)


# class Property(Base):
#     __tablename__ = "properties"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     comp_uuid = Column(String(80), nullable=False, unique=True, index=True)
#     prop_uuid = Column(String(80), nullable=False, unique=True, index=True)
#     view_uuid = Column(String(80),ForeignKey("views.view_uuid"), nullable=False, unique=True, index=True)
#     app_uuid = Column(String(80), ForeignKey("applications.app_uuid"), nullable=False, unique=True, index=True)
#     prop_name = Column(String(200), nullable=False)
#     prop_type = Column(String(200), nullable=False)
#     prop_value = Column(String(200), nullable=False)
#     user_id = Column(BigInteger, nullable=False,  index=True)
#     session_id = Column(String(200), nullable=False,  index=True)
#     created_datetime =Column(DateTime, nullable=False,  index=True,  default=func.now())
#     updated_datetime =Column(DateTime, nullable=False,  index=True, default=func.now())
#     updated_by =Column(String(80), nullable=False, unique=True, index=True)

#     def __repr__(self):
#         return 'CompModel(comp_id=%s,prop_uuid=%s, comp_uuid=%s,  view_uuid=%s, app_uuid=%s, prop_name=%s)' % \
#                (self.id, self.prop_uuid, self.comp_uuid, self.view_uuid, self.app_uuid, self.prop_name)




class Function(Base):
    __tablename__ = "function"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    func_uuid = Column(String(80), nullable=False, unique=True, index=True)
    key_name = Column(String(80), nullable=False, unique=True, index=True)
    desc = Column(String(200),nullable=False, unique=True, index=True)
    input_param = Column(String(300), nullable=False, unique=True, index=True)
    output_param = Column(String(800), nullable=False)

    def __repr__(self):
        return 'function(func_id=%s, key_name=%s,  desc=%s, input_param=%s, output_param=%s)' % \
               (self.id, self.key_name, self.desc, self.input_param, self.output_param)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)