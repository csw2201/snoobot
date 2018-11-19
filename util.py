from datetime import datetime, timedelta
import re
import pytz
from flask import json, Response

from conf.const import Const


class Util:
    @classmethod
    def get_day_str(cls, days=0):
        tz = pytz.timezone('Asia/Seoul')
        now = datetime.now(tz) + timedelta(days=days)
        day_str = now.strftime('%Y.%m.%d')
        return day_str

    @classmethod
    def get_time_str(cls, days=0):
        tz = pytz.timezone('Asia/Seoul')
        now = datetime.now(tz) + timedelta(days=days)
        day_str = now.strftime('%Y-%m-%d %H:%M:%S')
        return day_str

    @classmethod
    def send_response(cls, rst):
        json_string = json.dumps(rst)
        response = Response(json_string, content_type="application/json; charset=utf-8")
        return response

    @classmethod
    def show_start_menu(cls, msg='원하는 메뉴를 선택해 주세요', img_src=None):
        if img_src:
            rst = {
                "message": {
                    "text": msg,
                    "photo": {
                        "url": img_src,
                        'width': 640,
                        "height": 480
                    }
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": Const.DEFAULT_KEYBOARD
                }
            }
        else:
            rst = {
                "message": {
                    "text": msg
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": Const.DEFAULT_KEYBOARD
                }
            }
        return Util.send_response(rst)

    @classmethod
    def show_donate(cls):
        rst = {
            "message": {
                "text": '토스 QR & PayPal.me/payw/1',
                "photo": {
                    "url": "https://dl2.pushbulletusercontent.com/tWoO4jdenuRQdXvAWOjM7IXUhMM0z55S/1525226662706.jpg",
                    "width": 620,
                    "height": 620
                },
                "message_button": {
                    "label": "네이버페이",
                    "url": "http://npay.to/4c30232c7d9082e30f9c"
                }
            },
            "keyboard": {
                "type": "buttons",
                "buttons": Const.DEFAULT_KEYBOARD
            }
        }
        return Util.send_response(rst)

    @classmethod
    def is_img(cls, desc):
        result = re.match(r"https?://.*", desc)
        return result
