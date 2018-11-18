## resources/keyboard.py

from flask import json, Response
from flask_restful import Resource

from conf.const import Const


class Keyboard(Resource):
    @classmethod
    def get(cls):
        rst = {
            "type": "buttons",
            "buttons": Const.DEFAULT_KEYBOARD
        }
        json_string = json.dumps(rst)
        response = Response(json_string, content_type="application/json; charset=utf-8")
        return response
