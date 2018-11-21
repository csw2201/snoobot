from const import Const
import re


class Args:
    def __init__(self, args):
        self.args = args
        self.user_key = args.get(Const.ARG_USER_KEY)
        self.req_typ = args.get(Const.ARG_TYPE)
        content = args.get(Const.ARG_CONTENT)
        content = content.strip()
        self.content = re.sub('^#', '', content)
