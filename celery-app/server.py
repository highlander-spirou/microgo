from flask import Flask, request, make_response, send_file, jsonify
from errors import Error, Code
from controllers import upload_func, download_func
from instantiation import authenticator, file_access
# from lib import sign_user, validate_signature, upload_func, download_func, list_imgs
# from errors import Error
app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login_ctrl():
    if not request.authorization:
        return {"message": "Authorization header not found"}, 401
    
    signed_token = authenticator.sign_user(request.authorization.username, request.authorization.password)
    if not isinstance(signed_token, Error):
#     if signed_token is not None:
        resp = make_response({'message': 'Login sucess', 'token': signed_token})
        resp.headers['Authorization'] = 'Bearer ' + signed_token
        resp.status_code = 200

    else:
        resp = make_response({'message': signed_token.message})
        resp.status_code = 401

    return resp


@app.route('/upload', methods=['POST'])
def upload_ctrl():
    if "Authorization" not in request.headers:
        return {'message': "Authorization header not found"}, 401
    token = request.headers["Authorization"].split(" ")[1]

    verified_sig = authenticator.validate_signature(token)
    if isinstance(verified_sig, Error):
        return {'message': "Authorization failed"}, 500
    
    f = request.files['data']
    fs_id = upload_func(verified_sig['id'], f)
    return {'fs_id': fs_id}



@app.route('/download', methods=['POST'])
def download_ctrl():
    if "Authorization" not in request.headers:
        return {'message': "Authorization header not found"}, 401
    token = request.headers["Authorization"].split(" ")[1]

    verified_sig = authenticator.validate_signature(token)
    if isinstance(verified_sig, Error):
        return {'message': "Authorization failed"}, 500
    
    fs_id = request.get_json().get('fs_id')
    resp = download_func(fs_id, verified_sig['id'])
    if isinstance(resp, Error):
        if resp.err_code == Code.File_ReadError:
            return {'message': 'File not found'}, 400
        elif resp.err_code == Code.Download_Unauth:
            return {'message': 'Permission denied'}, 401
    
    return send_file(resp[1], download_name=resp[0])
    # if "Authorization" not in request.headers:
    #     return {'message': "Authorization not found"}, 401
    # token = request.headers["Authorization"].split(" ")[1]
    # verified_sig = validate_signature(token)
    # if fs_id is None:
    #     return {'message': 'Argument not found: `fs_id`'}, 400

    # resp = download_func(fs_id, verified_sig['username'])

    # if isinstance(resp, Error):
    #     # if resp.message ==
    #     return {'message': 'ID not found'}, 400
    # if resp is None:
    #     return {'message': 'Permission denied'}, 401
    

    # return send_file(resp[1], download_name=resp[0])


@app.route('/img_collection', methods=['GET'])
def img_collection_ctrl():
    if "Authorization" not in request.headers:
        return {'message': "Authorization header not found"}, 401
    token = request.headers["Authorization"].split(" ")[1]

    verified_sig = authenticator.validate_signature(token)
    if isinstance(verified_sig, Error):
        return {'message': "Authorization failed"}, 500
    
    fs_id_list = file_access.list_imgs(verified_sig['id'])
    return fs_id_list

    # if "Authorization" not in request.headers:
    #     return {'message': "Authorization not found"}, 401
    
    # token = request.headers["Authorization"].split(" ")[1]
    # verified_sig = validate_signature(token)

    # metadict = list_imgs(verified_sig['username'])
    # return jsonify(metadict)
    

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)