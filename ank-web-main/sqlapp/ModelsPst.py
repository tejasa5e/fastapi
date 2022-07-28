from sqlalchemy import BigInteger, Column, Integer, String, Float, ForeignKey,DateTime,Boolean
from dbsetup.postgres import Base
from sqlalchemy.sql import func

class Product(Base):
    __tablename__ = 'sa_products_master'

    product_id = Column(String, primary_key=True, index=True)
    product_name = Column(String, index=True)
    aisle_id = Column(String,  index=True)
    department_id = Column(String, index=True)

class Department(Base):
    __tablename__ = 'sa_departments_master'
	
    department_id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True)

class Aisle(Base):
    __tablename__ = 'sa_stores_aisel'
	
    aisle_id = Column(Integer, primary_key=True, index=True)
    aisle = Column(String, index=True)