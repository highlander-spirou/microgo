import requests
from flask import Request
from config import config
from typing import Tuple, TypeAlias

def login(request: Request):
    """
    Send request to a auth service, return a user state
    """
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{config.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth
    )
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    


json_string: TypeAlias = str
status_code: TypeAlias = int
def validate(request:Request) -> Tuple[None, Tuple[json_string, status_code]] :
    """
    Validate a login credentials using auth service
    """
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials", 401)

    response = requests.post(
        f"http://{config.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)