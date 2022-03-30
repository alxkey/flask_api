from flask import request
from jwt import encode, decode

from config import SECRET_KEY


def token_extraction():
    auth = request.headers.get('Authorization')   #########################  try except
    list_auth = auth.split()
    token = list_auth[1]
    return token


class TokenGen:
    def __init__(self):
        self.key = SECRET_KEY

    def generate(self, id):
        payload = {"user": id}
        token = encode(payload, self.key, algorithm="HS256")
        return token


class TokenCheck:
    def __init__(self, token, id):
        self.key = SECRET_KEY

    def __check(self, token, id):
        response = False
        payload = {"user": id}
        data = decode(token, self.key, algorithm="HS256")
        if data == payload:
            response = True
        return response


