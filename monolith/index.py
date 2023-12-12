from flask import Flask, request, make_response, send_file
from libs import sign_user, validate_signature, compress_img, create_fs, read_fs, delete_fs

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
    resp = create_fs('a', b'asdasf', 'sth')
    if resp[1] == 200:
        fs_id = resp[0]
        
    else:
        return resp
    # if "Authorization" not in request.headers:
    #     return {'message': "Authorization not found"}, 401
    # token = request.headers["Authorization"].split(" ")[1]
    # re = validate_signature(token)
    # if re[1] != 200:
    #     return re
    
    # username = re[0]['message']['username']
    # f = request.files['data']
    # upload_name = f"{username}-{f.filename}"
    # f.save("./uploads/" + upload_name)
    # compress_img(upload_name)

    # return {"message": "Upload successfully"}, 200



@app.route('/download', methods=['POST'])
def download_ctrl():
    if "Authorization" not in request.headers:
        return {'message': "Authorization not found"}, 401
    token = request.headers["Authorization"].split(" ")[1]
    re = validate_signature(token)
    base_path = './uploads/optimized/' + re['username'] + '-' + request.get_json().get('filename')
    return send_file(base_path)


@app.route('/img_collection', methods=['POST'])
def img_collection_ctrl():
    if "Authorization" not in request.headers:
        return {'message': "Authorization not found"}, 401
    

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)