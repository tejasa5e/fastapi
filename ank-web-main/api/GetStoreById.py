from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import pandas as pd
import os
from api import ApiUtils


def get_enriched_store(store_id):
    final_source_file_name = 'ca_stores.csv'
    source_dir = 'data'
    error_id = None
    result_json = None
    if store_id is not None:
        store_db = pd.read_csv(os.path.join(source_dir, final_source_file_name), index_col=False)
        # result_store = store_db[store_db['storeId'].str.contains(str(store_id))]
        result_store = store_db[store_db['storeId'] == int(store_id)]
        try:
            result_json = result_store.to_json(orient='records')[1:-1].replace('},{', '} {')
        except:
            error_id = 'Unable to parse selected store data'
    else:
        error_id = 'Bad Store ID'
    return result_json, error_id


def get_store_data(query_dict):
    '''
    :param
        query_dict: {store":"243"}
    :return:
        result_json: JSON result of the query
        error_id: error message
    '''
    store_id = None
    result_json = []
    error_id = 'Bad Store ID Request'
    for key, value in query_dict.items():
        if key == 'storeId':
            store_id = value
    if store_id is not None:
        result_json, error_id = get_enriched_store(store_id)
    return ApiUtils.generate_result_json(result_json, error_id)


# Pydantic data model class for Store Query By Id
class Query(BaseModel):
    '''
        storeId: String parameter
    '''
    storeId: str


def generate_query_response(query):
    query_dict = jsonable_encoder(query)
    return get_store_data(query_dict)
