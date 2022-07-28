

def generate_result_json(result_json, error_id):
    final_json = {'result': [], 'status': True, 'message': None}
    if error_id is None:
        final_json['result'] = result_json
        final_json['message'] = "Store Request is completed successfully."
    else:
        final_json['status'] = False
        final_json['message'] = error_id
    return final_json

