from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import pandas as pd
import os
from api import ApiUtils


def get_filtered_store(filter_name, filter_condition, filter_value, limit_result):
    '''
    :return:
        result_json: Json collection of filtered stores list
        error_id: Error message
    '''
    error_id = None
    result_json = None
    final_source_file_name = 'ca_stores.csv'
    source_dir = 'data'
    if filter_name in ['state', 'zipcode', 'city'] and filter_condition in ['==', '!=']:
        stores_db = pd.read_csv(os.path.join(source_dir, final_source_file_name), index_col=False)
        all_values = None
        if filter_condition == '==':
            all_values = stores_db[stores_db[filter_name] < filter_value]
        elif filter_condition == '!=':
            all_values = stores_db[stores_db[filter_name] <= filter_value]
        if all_values is not None:
            if limit_result > 10:
                limit_result = 10
            all_values = all_values.head(limit_result)
            try:
                result_json = all_values.to_json(orient='records')[1:-1].replace('},{', '} {')
            except:
                error_id = 'Unable to parse selected store data'
    else:
        error_id = 'Bad Stores Filters'

    return result_json, error_id


def get_store_data(query_dict):
    '''
    :param
        query_dict: In JSON format
            {"filterName":"state", "filterValue": "ca", "filterCondition": "==", "limitResult": 5}
    :return:
        result_json: JSON result of the query
        error_id: error message
    '''
    filter_name = None
    filter_value = 0
    filter_condition = None
    limit_result = None
    result_json = []
    error_id = 'Bad State ID Request'
    for key, value in query_dict.items():
        if key == 'filterName':
            filter_name = value
        elif key == 'filterValue':
            filter_value = value
        elif key == 'filterCondition':
            filter_condition = value
        elif key == 'limitResult':
            limit_result = value
    if None not in (filter_name, filter_condition, limit_result, filter_value):
        result_json, error_id = get_filtered_store(filter_name, filter_condition, filter_value, limit_result)
    return ApiUtils.generate_result_json(result_json, error_id)


# Pydantic data model class for Store Query By Filter
class Query(BaseModel):
    '''
        storeId: String parameter
    '''
    filterName: str
    filterCondition: str
    filterValue: str
    limitResult: int


def generate_query_response(query):
    query_dict = jsonable_encoder(query)
    return get_store_data(query_dict)