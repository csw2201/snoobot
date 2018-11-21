## evnets/result.py

import operator

from const import Const
from firebaseInit import fs
from util import Util
from args import Args
from select import Select


class Result(Args):
    def show_result(self):
        try:
            # 해당 그룹에서 가장 많이 나온 순서대로 보여준다.
            user = fs.collection(Const.COL_USER).document(self.user_key).get()
            user_group = user.get(Const.FIELD_GROUP)
        except:
            print('Not Found User Group')
            return Select(self.args).show_group_list()

        today = Util.get_day_str()
        today_format = '[{}]'.format(today)
        msg_list = [today_format]
        result_dict = {}
        try:
            result = fs.collection(Const.COL_SELECT).document(user_group).collection(Const.COL_TODAY).document(today).get()
            for user_key, restaurant in result._data.items():
                if restaurant in result_dict:
                    result_dict[restaurant] += 1
                else:
                    result_dict[restaurant] = 1

            sorted_list = sorted(result_dict.items(), key=operator.itemgetter(1))
            sorted_list.reverse()

            for item in sorted_list:
                title = item[0]
                count = item[1]
                msg_list.append('{}명 : {}'.format(count, title))
        except:
            print('Error')
            msg_list.append('아직 아무도 선택하지 않았습니다.')

        rst = {
            "message": {
                "text": '\n'.join(msg_list)
            },
            "keyboard": {
                "type": "buttons",
                "buttons": Const.DEFAULT_KEYBOARD
            }
        }

        return Util.send_response(rst)
