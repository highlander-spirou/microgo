from flask import Flask, request, make_response, send_file, jsonify
from libs import sign_user, validate_signature, upload_func, download_func, list_imgs
from dtypes import Error
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login_ctrl():
    if not request.authorization:
        return {"message": "Authorization header not found"}, 401
    
    message, status_code = sign_user(request.authorization.username, request.authorization.password)
    if status_code == 200:
        resp = make_response({'message': 'Login sucess'})
        resp.headers['Authorization'] = 'Bearer ' + message['message']
    else:
        resp = make_response(message)

    resp.status_code = status_code
    return resp


@app.route('/upload', methods=['POST'])
def upload_ctrl():
    if "Authorization" not in request.headers:
        return {'message': "Authorization not found"}, 401
    token = request.headers["Authorization"].split(" ")[1]
    verified_sig = validate_signature(token)
    if isinstance(verified_sig, Error):
        return {'message': "Authorization failed"}, 500
    
    f = request.files['data']
    resp = upload_func(verified_sig['username'], f)
    return resp



@app.route('/download', methods=['POST'])
def download_ctrl():
    if "Authorization" not in request.headers:
        return {'message': "Authorization not found"}, 401
    token = request.headers["Authorization"].split(" ")[1]
    verified_sig = validate_signature(token)
    fs_id = request.get_json().get('fs_id')
    if fs_id is None:
        return {'message': 'Argument not found: `fs_id`'}, 400

    resp = download_func(fs_id, verified_sig['username'])

    if isinstance(resp, Error):
        return {'message': 'ID not found'}, 400
    if resp is None:
        return {'message': 'Permission denied'}, 401
    

    return send_file(resp[1], download_name=resp[0])


@app.route('/img_collection', methods=['GET'])
def img_collection_ctrl():
    if "Authorization" not in request.headers:
        return {'message': "Authorization not found"}, 401
    
    token = request.headers["Authorization"].split(" ")[1]
    verified_sig = validate_signature(token)

    metadict = list_imgs(verified_sig['username'])
    return jsonify(metadict)
    

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)