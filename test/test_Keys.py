__author__ = 'kmadac'

import UserManagement.Keys as Keys
import unittest
import UserManagement.BaseFilerApi
import os

class Test_Keys(unittest.TestCase):
    def setUp(self):
        self.netappkeys = Keys.Keys('./keys', '10.228.167.98', os.environ['FILERPASS'])

    def test_dir_create(self):
        r = self.netappkeys.create_dir(path='/vol/ROOT/etc/sshd/kmadac')
        self.assertEqual(r, '/vol/ROOT/etc/sshd/kmadac')

    def test_dir_struct_create(self):
        r = self.netappkeys._create_dir_structure('kmadac')
        self.assertEqual(r, '/vol/ROOT/etc/sshd/kmadac/.ssh')

    def test_deploy_key(self):
        r = self.netappkeys.deploy_key('kmadac')
        self.assertEqual(r, True)

    def test_api_delete_file(self):
        self.assertRaises(UserManagement.BaseFilerApi.deleteFileNotFoundException,
                          self.netappkeys.delete_file, ('/vol/ROOT/etc/sshd/kmadac/.ssh/doesnt_exist'))

        self.assertRaises(UserManagement.BaseFilerApi.deleteFileNotFoundException,
                          self.netappkeys.delete_file, ('/vol/ROOT/etc/sshd/authorized_keys2'))

        self.netappkeys.create_file('/vol/ROOT/etc/sshd/testfile.dat',"test")

        r = self.netappkeys.delete_file('/vol/ROOT/etc/sshd/testfile.dat')
        self.assertEqual(r, True)

    def test_delete_key(self):
        r = self.netappkeys.delete_key('kmadac')
        self.assertEqual(r, True)

if __name__ == '__main__':
    unittest.main()
