from flask import Flask, request, make_response, send_file, jsonify
from errors import Error
from controllers import upload_func
from instantiation import authenticator
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
    print(verified_sig)
    if isinstance(verified_sig, Error):
        return {'message': "Authorization failed"}, 500
    
    f = request.files['data']
    upload_func(verified_sig['id'], f)
    return "hello"
    # resp = upload_func(verified_sig['username'], f)
    # return resp



# @app.route('/download', methods=['POST'])
# def download_ctrl():
#     if "Authorization" not in request.headers:
#         return {'message': "Authorization not found"}, 401
#     token = request.headers["Authorization"].split(" ")[1]
#     verified_sig = validate_signature(token)
#     fs_id = request.get_json().get('fs_id')
#     if fs_id is None:
#         return {'message': 'Argument not found: `fs_id`'}, 400

#     resp = download_func(fs_id, verified_sig['username'])

#     if isinstance(resp, Error):
#         # if resp.message ==
#         return {'message': 'ID not found'}, 400
#     if resp is None:
#         return {'message': 'Permission denied'}, 401
    

#     return send_file(resp[1], download_name=resp[0])


# @app.route('/img_collection', methods=['GET'])
# def img_collection_ctrl():
#     if "Authorization" not in request.headers:
#         return {'message': "Authorization not found"}, 401
    
#     token = request.headers["Authorization"].split(" ")[1]
#     verified_sig = validate_signature(token)

#     metadict = list_imgs(verified_sig['username'])
#     return jsonify(metadict)
    

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)