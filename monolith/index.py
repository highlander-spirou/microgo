from flask import Flask, request, make_response, send_file
from libs import download_func, upload_func, sign_user, validate_signature, compress_img

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
    re = validate_signature(token)
    f = request.files['data']
    upload_name = f"{re['username']}-{f.filename}"
    f.save("./uploads/" + upload_name)
    compress_img(upload_name)

    return {"message": "Upload successfully"}, 200



@app.route('/download', methods=['POST'])
def download_ctrl():
    if "Authorization" not in request.headers:
        return {'message': "Authorization not found"}, 401
    token = request.headers["Authorization"].split(" ")[1]
    re = validate_signature(token)
    base_path = './uploads/optimized/' + re['username'] + '-' + request.get_json().get('filename')
    return send_file(base_path)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)