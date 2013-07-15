__author__ = 'kmadac'

import os, random, string
from BaseFilerApi import BaseFilerApi, createUserAlreadyExistsException


class FilerUsers(BaseFilerApi):
    def __init__(self, filer, password, login='root'):
        BaseFilerApi.__init__(self, filer=filer, login=login, password=password)

    def _gen_pass(self):
        length = 11
        chars = string.ascii_letters + string.digits + '@#$%*'
        random.seed = (os.urandom(1024))

        return ''.join(random.choice(chars) for i in range(length)) + '1'

    def create_user(self, user_names, password='', full_name=''):
        """
        Create user/s on filer.
        If user_names is string, it will create one user
        If user_names is list, it will create all users in list
        """
        users = []
        if isinstance(user_names, str):
            users = [user_names]
        else:
            users = user_names

        for user in users:
            if password == '':
                password = self._gen_pass()
            try:
                super(FilerUsers, self).create_user(user, password)
            except createUserAlreadyExistsException:
                pass

        return True

    def delete_user(self, user_names):
        """
        delete user/s from filer
        If user_names is string, it will delete one user
        If user_names is list, it will delete all users in list
        """
        users = []
        if isinstance(user_names, str):
            users = [user_names]
        else:
            users = user_names

        for user in users:
            super(FilerUsers, self).delete_user(user)

        return True
