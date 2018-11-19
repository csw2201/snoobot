## resources/message.py

from flask_restful import reqparse

from conf.firebaseInit import fs
from conf.util import Util
from events.result import Result
from events.select import Select
from events.setting import Setting
from resources.keyboard import *

parser = reqparse.RequestParser()
parser.add_argument('user_key', type=str, required=True)
parser.add_argument('type', type=str, required=True)
parser.add_argument('content', type=str, required=True)


class Message(Resource):
    def __init__(self):
        self.args = parser.parse_args()
        self.user_key = self.args[Const.ARG_USER_KEY]
        self.req_type = self.args[Const.ARG_TYPE]
        self.content = self.args[Const.ARG_CONTENT]

    def post(self):
        select = Select(self.args)
        setting = Setting(self.args)
        result = Result(self.args)

        if self.content == Const.BTN_SELECT_LUNCH:
            return select.show_restaurant_list()
        elif self.content == Const.BTN_GOTO_START:
            return Util.show_start_menu()
        elif self.content == Const.BTN_SETTING:
            return setting.show_setting_list()
        elif self.content == Const.BTN_SETTING_GROUP:
            return select.show_group_list()
        elif self.content == Const.BTN_SEE_RESULT:
            return result.show_result()
        elif self.content == Const.BTN_ADD_RESTAURANT:
            return setting.show_add_restaurant()
        elif self.content == Const.BTN_ADD_RESTAURANT_CONFIRM:
            return setting.add_restaurant()
        elif self.content == Const.BTN_DELETE_RESTAURANT:
            return setting.show_delete_restaurant()
        elif self.content == Const.BTN_DELETE_RESTAURANT_CONFIRM:
            return setting.delete_restaurant()
        elif self.content == Const.BTN_DOANTE:
            return Util.show_donate()

        # 사용자 입력처리
        user = fs.collection(Const.COL_USER).document(self.user_key).get()
        user_state = user.get(Const.FIELD_STATE)

        if user_state == Const.STATE_SELECT_GROUP:
            return select.group_selected()
        elif user_state == Const.STATE_SELECT_RESTAURANT:
            return select.restaurant_selected()
        elif user_state == Const.STATE_ADD_RESTAURANT_TITLE:
            return setting.show_add_restaurant_desc()
        elif user_state == Const.STATE_ADD_RESTAURANT_DESC:
            return setting.show_add_restaurant_confirm()
        elif user_state == Const.STATE_DELETE_RESTAURANT:
            return setting.show_delete_restaurant_confirm()

        # default
        return Util.show_start_menu()
