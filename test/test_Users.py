__author__ = 'kmadac'

import unittest
import UserManagement.FilerUsers as Users
import UserManagement.BaseFilerApi


class Test_UserManagement(unittest.TestCase):
    def setUp(self):
        self.netappapi = Users.FilerUsers('10.228.167.98', 'nasrise1')

    def test_create_delete_user(self):
        r = False
        try:
            r = self.netappapi.create_user('kmadac')
        except UserManagement.BaseFilerApi.createUserAlreadyExistsException:
            pass
        self.assertEqual(r, True)

        r = False
        try:
            r = self.netappapi.delete_user('kmadac')
        except UserManagement.BaseFilerApi.deleteUserException:
            pass
        self.assertEqual(r, True)

#        r = self.netappapi.delete_user('nonexist')
        self.assertRaises(UserManagement.BaseFilerApi.deleteUserNotFoundException, self.netappapi.delete_user, 'nonexist')

    def test_UserList(self):
        r = False
        try:
            r = self.netappapi.list_users()
        except UserManagement.BaseFilerApi.listUsersException:
            pass

        print r

if __name__ == '__main__':
    unittest.main()
