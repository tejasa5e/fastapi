import pandas as pd
import os
from api import ApiUtils


def get_data():
    final_source_file_name = 'ca_stores.csv'
    source_dir = 'data'
    error_id = None
    result_json = None
    stores_db = pd.read_csv(os.path.join(source_dir, final_source_file_name), index_col=False)
    result_store = stores_db.sample(5)['storeId']
    try:
        result_json = result_store.to_json(orient='records')[1:-1].replace('},{', '} {')
    except:
        error_id = 'Unable to get store data'
    return result_json, error_id


def get_store_ids_list():
    '''
    :param
    :return:
        result_json: JSON result of the query
        error_id: error message
    '''
    result_json, error_id = get_data()
    return ApiUtils.generate_result_json(result_json, error_id)


def generate_query_response():
    return get_store_ids_list()
