## evnets/setting.py
from firebase_admin import firestore

from conf.const import Const
from conf.firebaseInit import fs
from conf.util import Util
from events.args import Args
from events.select import Select


class Setting(Args):
    def show_setting_list(self):
        try:
            user = fs.collection(Const.COL_USER).document(self.user_key).get()
            group = user.get(Const.FIELD_GROUP)
        except:
            return Select.show_group_list()

        rst = {
            "message": {
                "text": '현재 [{}] 그룹으로 설정되어 있습니다.'.format(group)
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [Const.BTN_ADD_RESTAURANT, Const.BTN_DELETE_RESTAURANT, Const.BTN_SETTING_GROUP, Const.BTN_DOANTE, Const.BTN_GOTO_START]
            }
        }
        return Util.send_response(rst)

    def show_add_restaurant(self):
        # state : add_restaurant
        # 1. 이름을 입력해 주세요
        # 2. 설명을 작성해 주세요.
        # 상태 설정
        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_STATE: Const.STATE_ADD_RESTAURANT_TITLE
        }, firestore.CreateIfMissingOption(True))

        rst = {
            "message": {
                "text": '음식점 이름을 입력해 주세요'
            }
        }

        return Util.send_response(rst)

    def show_add_restaurant_desc(self):
        # content = 음식점 이름
        # 상태 설정
        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_STATE: Const.STATE_ADD_RESTAURANT_DESC
        }, firestore.CreateIfMissingOption(True))

        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_ADD_RESTAURANT_TITLE: self.content
        })

        rst = {
            "message": {
                "text": '음식점 사진을 추가해 주세요'
            }
        }

        return Util.send_response(rst)

    def show_add_restaurant_confirm(self):
        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_STATE: Const.STATE_ADD_RESTAURANT_CONFIRM
        }, firestore.CreateIfMissingOption(True))

        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_ADD_RESTAURANT_DESC: self.content
        }, firestore.CreateIfMissingOption(True))

        user = fs.collection(Const.COL_USER).document(self.user_key).get()
        title = user.get(Const.FIELD_ADD_RESTAURANT_TITLE)
        desc = self.content

        if Util.is_img(desc):
            rst = {
                "message": {
                    "text": '입력하신 음식점은 다음과 같습니다.\n\n이름:{}\n\n등록하시겠습니까?'.format(title),
                    "photo": {
                        "url": desc,
                        "width": 640,
                        "height": 480
                    }
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": [
                        Const.BTN_ADD_RESTAURANT_CONFIRM,
                        Const.BTN_GOTO_START
                    ]
                }
            }
        else:
            rst = {
                "message": {
                    "text": '입력하신 음식점은 다음과 같습니다.\n\n이름:{}\n설명:{}\n\n등록하시겠습니까?'.format(title, desc)
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": [
                        Const.BTN_ADD_RESTAURANT_CONFIRM,
                        Const.BTN_GOTO_START
                    ]
                }
            }

        return Util.send_response(rst)

    def add_restaurant(self):
        user = fs.collection(Const.COL_USER).document(self.user_key).get()
        group = user.get(Const.FIELD_GROUP)
        title = user.get(Const.FIELD_ADD_RESTAURANT_TITLE)
        desc = user.get(Const.FIELD_ADD_RESTAURANT_DESC)

        try:
            ref = fs.collection(Const.COL_GROUP).document(group).get()
            restaurant = ref._data.get(Const.FIELD_RESTAURANT)
        except:
            restaurant = {}

        if restaurant is None:
            restaurant = {}

        restaurant[title] = {
            'desc': desc,
            'user': self.user_key,
            'added': Util.get_day_str()
        }

        if Util.is_img(desc):
            restaurant[title][Const.FIELD_IMG_SRC] = desc

        fs.collection(Const.COL_GROUP).document(group).update({Const.FIELD_RESTAURANT: restaurant}, firestore.CreateIfMissingOption(True))

        if Util.is_img(desc):
            msg = '[{}] 이(가) 등록되었습니다'.format(title)
            return Util.show_start_menu(msg, desc)

        msg = '이름:{}\n설명:{}\n등록되었습니다'.format(title, desc)
        return Util.show_start_menu(msg)

    def show_delete_restaurant(self):
        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_STATE: Const.STATE_DELETE_RESTAURANT
        }, firestore.CreateIfMissingOption(True))

        user = fs.collection(Const.COL_USER).document(self.user_key).get()
        group = user.get(Const.FIELD_GROUP)

        ref = fs.collection(Const.COL_GROUP).document(group).get()
        restaurants = ref._data.get(Const.FIELD_RESTAURANT)

        restaurant_list = []
        for key, val in restaurants.items():
            restaurant_list.append(key)

        restaurant_list.append(Const.BTN_GOTO_START)

        rst = {
            "message": {
                "text": '삭제할 대상을 선택해 주세요'
            },
            "keyboard": {
                "type": "buttons",
                "buttons": restaurant_list
            }
        }

        return Util.send_response(rst)

    def show_delete_restaurant_confirm(self):
        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_STATE: Const.STATE_DELETE_RESTAURANT
        }, firestore.CreateIfMissingOption(True))

        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_DELETE_RESTAURANT_TITLE: self.content
        }, firestore.CreateIfMissingOption(True))

        title = self.content

        rst = {
            "message": {
                "text": '[{}] 을(를) 삭제하겠습니까?'.format(title)
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    Const.BTN_DELETE_RESTAURANT_CONFIRM,
                    Const.BTN_GOTO_START
                ]
            }
        }

        return Util.send_response(rst)

    def delete_restaurant(self):
        user = fs.collection(Const.COL_USER).document(self.user_key).get()
        group = user.get(Const.FIELD_GROUP)
        title = user.get(Const.FIELD_DELETE_RESTAURANT_TITLE)

        try:
            ref = fs.collection(Const.COL_GROUP).document(group).get()
            restaurant = ref._data.get(Const.FIELD_RESTAURANT)
            del restaurant[title]
        except:
            restaurant = {}

        fs.collection(Const.COL_GROUP).document(group).update({Const.FIELD_RESTAURANT: restaurant}, firestore.CreateIfMissingOption(True))

        msg = '[{}] 을(를) 삭제하였습니다.'.format(title)
        return Util.show_start_menu(msg)
