## events/select.py

import operator
from random import shuffle

from firebase_admin import firestore

from conf.const import Const
from conf.firebaseInit import fs
from conf.util import Util
from events.args import Args


class Select(Args):
    def show_group_list(self):
        # 상태 설정
        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_STATE: Const.STATE_SELECT_GROUP
        }, firestore.CreateIfMissingOption(True))

        # 그룹 목록 가져오기
        groups = fs.collection(Const.COL_GROUP).get()
        group_list = []
        for doc in groups:
            group_list.append(doc.id)

        group_list.append(Const.BTN_GOTO_START)

        rst = {
            "message": {
                "text": '그룹을 선택해 주세요'
            },
            "keyboard": {
                "type": "buttons",
                "buttons": group_list
            }
        }

        return Util.send_response(rst)

    def group_selected(self):
        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_GROUP: self.content
        }, firestore.CreateIfMissingOption(True))

        msg = '[{}] 을(를) 선택하였습니다'.format(self.content)
        return Util.show_start_menu(msg)

    def show_restaurant_list(self):
        # 상태 설정
        fs.collection(Const.COL_USER).document(self.user_key).update({
            Const.FIELD_STATE: Const.STATE_SELECT_RESTAURANT
        }, firestore.CreateIfMissingOption(True))

        # 그룹이 없으면 그룹 선택으로 보낸다.
        try:
            user = fs.collection(Const.COL_USER).document(self.user_key).get()
            user_group = user.get(Const.FIELD_GROUP)
        except:
            print("NotFound user")
            return self.show_group_list()

        try:
            # 해당 그룹의 식당목록을 가져온다.
            restaurant_list = []

            group = fs.collection(Const.COL_GROUP).document(user_group).get()
            restaurants = group.get(Const.FIELD_RESTAURANT)
            for key, val in restaurants.items():
                restaurant_list.append(key)
        except:
            print('No RESTAURANTS')
            return Util.show_start_menu('등록된 식당이 없습니다')

        shuffle(restaurant_list)

        if len(restaurant_list) > Const.SHOW_COUNT:
            restaurant_list = restaurant_list[:Const.SHOW_COUNT]

        restaurant_list.append(Const.BTN_GOTO_START)

        rst = {
            "message": {
                "text": '식당을 선택해 주세요'
            },
            "keyboard": {
                "type": "buttons",
                "buttons": restaurant_list
            }
        }

        return Util.send_response(rst)

    def restaurant_selected(self):
        user = fs.collection(Const.COL_USER).document(self.user_key).get()
        user_group = user.get(Const.FIELD_GROUP)
        today = Util.get_day_str()

        fs.collection(Const.COL_SELECT).document(user_group).collection(Const.COL_TODAY).document(today).update({
            self.user_key: self.content
        }, firestore.CreateIfMissingOption(True))

        msg = '[{}] 을(를) 선택하였습니다'.format(self.content)

        try:
            ref = fs.collection(Const.COL_GROUP).document(user_group).get()
            restaurants = ref._data.get(Const.FIELD_RESTAURANT)
            target = restaurants.get(self.content)
            img_src = target.get(Const.FIELD_IMG_SRC)
        except:
            img_src = None

        return Util.show_start_menu(msg, img_src)

    def create_history(self, today):
        user = fs.collection(Const.COL_USER).document(self.user_key).get()
        user_group = user.get(Const.FIELD_GROUP)

        # 오늘 기준
        # 5일 전까지 고려
        title_list = []
        for i in range(1, 5 + 1):
            ago_day = Util.get_day_str(-1 * i)
            max_title = self.get_max_selected_restaurant(user_group, ago_day)
            if max_title:
                title_list.append(max_title)

        fs.collection(Const.COL_SELECT).document(user_group).collection(Const.COL_HISTORY).document(today).update({
            Const.FIELD_MAX_HISTORY_LIST: title_list
        }, firestore.CreateIfMissingOption(True))

        return title_list

    @classmethod
    def get_max_selected_restaurant(cls, user_group, day):
        result_dict = {}
        try:
            result = fs.collection(Const.COL_SELECT).document(user_group).collection(Const.COL_TODAY).document(day).get()
            for user_key, restaurant in result._data.items():
                if restaurant in result_dict:
                    result_dict[restaurant] += 1
                else:
                    result_dict[restaurant] = 1

            sorted_list = sorted(result_dict.items(), key=operator.itemgetter(1))
            sorted_list.reverse()
            title = sorted_list[0][0]
        except:
            title = None

        return title
