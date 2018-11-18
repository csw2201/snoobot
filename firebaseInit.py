import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(FILE_DIR, 'snoobot-222810-3a2bad76258e.json')

# Use a service account
cred = credentials.Certificate(CONFIG_PATH)
firebase_admin.initialize_app(cred)

fs = firestore.client()
class Const:
  COL_GROUP = 'group'
  COL_USER = 'user'
  COL_SELECT = 'select'
  COL_TODAY = 'today'

  FIELD_TITLE = 'title'
  FIELD_GROUP = 'group'
  FIELD_STATE = 'state'
  FIELD_RESTAURANT = 'restaurant'
  FIELD_ADD_RESTAURANT_TITLE = 'add_restaurant_title'
  FIELD_ADD_RESTAURANT_DESC = 'add_restaurant_desc'
  FIELD_DELETE_RESTAURANT_TITLE = 'delete_restaurant_title'
  FIELD_MAX_HISTORY_LIST = 'daily_max_list'
  FIELD_IMG_SRC = 'img_src'

  STATE_SELECT_RESTAURANT = 'select_restaurant'
  STATE_SELECT_GROUP = 'select_group'
  STATE_ADD_RESTAURANT = 'add_restaurant'
  STATE_ADD_RESTAURANT_DESC = 'add_restaurant_desc'
  STATE_ADD_RESTAURANT_CONFIRM = 'add_restaurant_confirm'
  STATE_DELETE_RESTAURANT = 'delete_restaurant'
  STATE_DELETE_RESTAURANT_CONFIRM = 'delete_restaurant_confirm'

  ARG_USER_KEY = "user_key"
  ARG_TYPE = 'type'
  ARG_CONTENT = 'content'

  ## buttons
  BTN_SELECT_LUNCH = "#점심 선택"
  BTN_SEE_RESULT = "#결과 보기"
  BTN_SETTING = '#설정'

  DEFAULT_KEYBOARD = [BTN_SELECT_LUNCH, BTN_SEE_RESULT, BTN_SETTING]

  BTN_GOTO_START = "#처음으로"
  BTN_SETTING_GROUP = '#그룹 설정'
  BTN_ADD_RESTAURANT = "#식당 등록"
  BTN_ADD_RESTAURANT_CONFIRM = "#식당 등록 확인"
  BTN_DELETE_RESTAURANT = '#식당 삭제'
  BTN_DELETE_RESTAURANT_CONFIRM = '#식당 삭제 확인'
  BTN_DOANTE = '#후원 하기'
  
  SHOW_COUNT = 7
