from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Location where the sqllite data file will be stored on the disk
SQL_ALCHEMY_DATABASE_URL = "sqlite:///./dbsetup/ank.db"


engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_bootstrap_ddl ():
    DDL="""
        PRAGMA foreign_keys = off;
        BEGIN TRANSACTION;
        CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY AUTOINCREMENT, app_uuid VARCHAR (50), app_name VARCHAR (100), user_uid VARCHAR (80), created_datetime DATETIME, updated_datetime DATETIME, session_id VARCHAR (80), updated_by VARCHAR (80));
        DELETE FROM applications;
        INSERT INTO applications (id, app_uuid, app_name, user_uid, created_datetime, updated_datetime, session_id, updated_by) VALUES (27, '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', 'application 1', 'johndoe', '2022-07-21 06:41:05', '2022-07-21 06:41:05', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL);

        CREATE TABLE IF NOT EXISTS components (id INTEGER PRIMARY KEY AUTOINCREMENT, comp_uuid VARCHAR (50), comp_name VARCHAR (100), view_uuid VARCHAR (50) REFERENCES views (view_uuid), app_uuid VARCHAR (50) REFERENCES applications (app_uuid), created_datetime DATETIME, updated_datetime DATETIME, user_uid VARCHAR (100), session_id VARCHAR (200), updated_by VARCHAR (100), meta_data VARCHAR (400), properties VARCHAR (500));
        DELETE FROM components ;
        INSERT INTO components (id, comp_uuid, comp_name, view_uuid, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by, meta_data, properties) VALUES (20, 'a073787-dfcb-70e1-73c4-1b58c38650c', 'Header', '56ed6b6-1833-1dea-f0da-f04426b6bd75', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 06:46:00', '2022-07-21 06:46:00', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL, '{"text":"Heading","as":"h2","size":"xl","textAlign":"center"}', '{"height":"47px","width":"475px","x":10,"y":11}');
        INSERT INTO components (id, comp_uuid, comp_name, view_uuid, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by, meta_data, properties) VALUES (21, '5cdccf7-6b6f-2402-4c66-37c36c650c6', 'Image', '56ed6b6-1833-1dea-f0da-f04426b6bd75', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 06:46:00', '2022-07-21 06:46:00', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL, '{"src":"https://images.unsplash.com/photo-1600585154084-4e5fe7c39198?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OXx8aG91c2UlMjBpbnRlcmlvcnxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60","alt":"Dan Abramov"}', '{"height":"295px","width":"479px","x":7,"y":70}');
        INSERT INTO components (id, comp_uuid, comp_name, view_uuid, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by, meta_data, properties) VALUES (22, '28e4b60-485b-53a4-3a82-e3b5d20d766f', 'Header', '2b42d87-ed2-ed-83b5-71ffc6c223', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 06:46:44', '2022-07-21 06:46:44', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL, '{"text":"Heading da-da","as":"h2","size":"xl","textAlign":"left"}', '{"height":"57px","width":"302px","x":17,"y":22}');
        INSERT INTO components (id, comp_uuid, comp_name, view_uuid, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by, meta_data, properties) VALUES (23, 'c3e0d8a-e54-e6a1-e0df-2e2451cae7', 'Textarea', '56ed6b6-1833-1dea-f0da-f04426b6bd75', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 06:49:20', '2022-07-21 06:49:20', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL, '{"value":"Your content goes here....da-da","size":"xs","variant":"filled","functionbinding":{"func_uuid":"43190a71-876e-43b7-bc58-52f28a31867f","key_name":"GetProductsByAisle","desc":"string","input_param":{"aisle_id":"2"},"output_param":"product_id"}}', '{"height":"81px","width":"467px","x":12.666656494140625,"y":379.3333435058594}');

        CREATE TABLE  IF NOT EXISTS function (id INTEGER PRIMARY KEY AUTOINCREMENT, func_uuid VARCHAR (80), key_name VARCHAR (100), "desc" VARCHAR (300), input_param VARCHAR (300), output_param VARCHAR (500));
        DELETE FROM function  ;
        INSERT INTO function (id, func_uuid, key_name, "desc", input_param, output_param) VALUES (2, '8888c56a-b072-482b-89c0-2178f3f71eb8', 'GetProductsByDept', 'Get Products by Department', '[{"name":"Deparment ID","label":"dept_id", "type":"integer", "default" : 13 }]', '[{"name":"Product List","label":"product_list", "type":"list" }, {"name":"Product Name","label":"product_name", "type":"string" }, {"name":"Product ID","label":"product_id", "type":"integer" },{"name":"Department ID","label":"department_id", "type":"integer" },{"name":"Aisle ID","label":"aisle_id", "type":"integer" } ]');
        INSERT INTO function (id, func_uuid, key_name, "desc", input_param, output_param) VALUES (3, '43190a71-876e-43b7-bc58-52f28a31867f', 'GetProductsByAisle', 'string', '[{"name":"Aisle ID","label":"aisle_id", "type":"integer", "default" : 3 }]', '[{"name":"Product List","label":"product_list", "type":"list" }, {"name":"Product Name","label":"product_name", "type":"string" }, {"name":"Product ID","label":"product_id", "type":"integer" },{"name":"Department ID","label":"department_id", "type":"integer" },{"name":"Aisle ID","label":"aisle_id", "type":"integer" } ]');
        INSERT INTO function (id, func_uuid, key_name, "desc", input_param, output_param) VALUES (4, '21e709ff-6490-489c-9a2f-d52ca6f2b350', 'GetDepartmentList', 'Get department List', '[]', '[{"name":"Product List","label":"department_list", "type":"list" }, {"name":"Deparment Name","label":"department", "type":"string" },{"name":"Department ID","label":"department_id", "type":"integer" }]');
        INSERT INTO function (id, func_uuid, key_name, "desc", input_param, output_param) VALUES (5, '5352dd49-5411-482a-8b54-955bcabf0a69', 'GetAisleList', 'Get aisle list', '[]', '[{"name":"Aisle List","label":"aisle_list", "type":"list" }, {"name":"Aisle Name","label":"aisle", "type":"string" },{"name":"Aisle ID","label":"aisle_id", "type":"integer" } ]');

        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR (100), hashed_password VARCHAR (100), email VARCHAR (100), full_name VARCHAR (100), disabled BOOLEAN);
        DELETE FROM users   ;
        INSERT INTO users (id, username, hashed_password, email, full_name, disabled) VALUES (1, 'johndoe', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'johndoe@example.com', 'John Doe', 'False');

        CREATE TABLE IF NOT EXISTS views (id INTEGER PRIMARY KEY AUTOINCREMENT, view_uuid VARCHAR (100), view_name VARCHAR (100), app_uuid VARCHAR (50) REFERENCES applications (app_uuid), created_datetime DATETIME, updated_datetime DATETIME, user_uid VARCHAR (100), session_id VARCHAR (200), updated_by VARCHAR (100),  preview_id  VARCHAR (50));
        DELETE FROM views   ;        
        INSERT INTO views (id, view_uuid, view_name, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by,preview_id) VALUES (45, '56ed6b6-1833-1dea-f0da-f04426b6bd75', 'view0', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 06:41:12', '2022-07-21 06:41:12', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL,'kllw9ukgh2m');
        INSERT INTO views (id, view_uuid, view_name, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by,preview_id) VALUES (46, '2b42d87-ed2-ed-83b5-71ffc6c223', 'view1', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 06:46:09', '2022-07-21 06:46:09', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL,'491w9ukght');
        INSERT INTO views (id, view_uuid, view_name, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by,preview_id) VALUES (47, '4b37821-8e2d-fc57-431e-34dd75861da7', 'view2', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 14:58:01', '2022-07-21 14:58:01', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL,'104w9ukghn');
        INSERT INTO views (id, view_uuid, view_name, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by,preview_id) VALUES (48, '67d31ff-8260-2e6d-b0d4-bbdb7a633716', 'view3', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 15:04:25', '2022-07-21 15:04:25', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL,'pt5w9ukghk');
        INSERT INTO views (id, view_uuid, view_name, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by,preview_id) VALUES (49, '5ba8454-4458-ba13-8f6f-f1a81f15', 'view4', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 15:04:31', '2022-07-21 15:04:31', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL,'084w9ukghh');
        INSERT INTO views (id, view_uuid, view_name, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by,preview_id) VALUES (50, 'cd117-cbd-35c-0cec-806165351162', 'view5', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 15:04:35', '2022-07-21 15:04:35', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL,'345w9uvbn6');
        INSERT INTO views (id, view_uuid, view_name, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by,preview_id) VALUES (51, 'f13ccb-a242-a375-7ed6-64b83168330', 'view6', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 15:04:39', '2022-07-21 15:04:39', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU',NULL,'876w9ukgh2');
        INSERT INTO views (id, view_uuid, view_name, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by,preview_id) VALUES (52, 'e1435e-02b2-08e-dab3-f5a5ae25f36', 'view7', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 15:04:43', '2022-07-21 15:04:43', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL,'903w9uaut6');
        INSERT INTO views (id, view_uuid, view_name, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by,preview_id) VALUES (53, '87350a2-cbd0-0cb0-0a78-a275cca0f6', 'view8', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 15:04:47', '2022-07-21 15:04:47', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL,'571w9uars2');
        INSERT INTO views (id, view_uuid, view_name, app_uuid, created_datetime, updated_datetime, user_uid, session_id, updated_by,preview_id) VALUES (54, 'c48e7f-0a5-32ef-c32a-106d3887e8e4', 'view9', '1dfcb22-c813-d8e-d5ae-72415ca4bbbe', '2022-07-21 15:04:54', '2022-07-21 15:04:54', 'johndoe', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjU4Mzg3MTQxfQ.GQiPBo9W4QEz_BI9RrmiHPHfYOPYYbSfmNl_RpmYcZU', NULL, '261v9oars2');

        COMMIT TRANSACTION;
        PRAGMA foreign_keys = on;
        """
    return DDL