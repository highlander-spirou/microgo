from flask import Flask, request, make_response
from libs import download_func, convert_func, upload_func, sign_user, validate_signature

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



@app.route('/validate', methods=['POST'])
def validate_ctrl():
    pass


@app.route('/upload', methods=['POST'])
def upload_ctrl():
    # try:
    token = request.headers["Authorization"].split(" ")[1]
    re = validate_signature(token)
    
    return re
    # except Exception as e:
    #     return {'message': "con cặc"}, 401
    # if (request.headers["Authorization"].split(" ")[1]):
    #     return "con cặc", 401
    # else:
    #     print('cahfskaj')
    #     # print(token)
    # return "afskjhakj"



@app.route('/download', methods=['POST'])
def download_ctrl():
    pass


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)