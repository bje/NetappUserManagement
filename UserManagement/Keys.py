__author__ = 'kmadac'

import posixpath
import os
from os.path import join
from BaseFilerApi import BaseFilerApi, deleteDirNotFoundException, deleteFileNotFoundException


class DeployKeyException(Exception): pass


class Keys(BaseFilerApi):
    def __init__(self, path_to_keys, filer, password, login='root', root_volume_name='ROOT'):
        BaseFilerApi.__init__(self, filer=filer, login=login, password=password)
        self.root_volume_name = root_volume_name
        self.path_to_keys = path_to_keys
        self.key_file_name = 'id_rsa.pub'

    def _create_dir_structure(self, username):
        """
        Create directory structure for authorized keys file over API
        """
        userpath = posixpath.join('/vol', self.root_volume_name, 'etc', 'sshd', username)
        sshpath = posixpath.join('/vol', self.root_volume_name, 'etc', 'sshd', username,'.ssh')

        r = self.create_dir(userpath)
        if r:
            r = self.create_dir(sshpath)

        return sshpath

    def get_users(self):
        """
        Returns directories in directory self.path_to_keys and it is list of usernames
        """
        return [d for d in os.listdir(self.path_to_keys) if os.path.isdir(os.path.join(self.path_to_keys, d))]

    def is_key_avail(self, username):
        """
        Return True if directory username exists in path_to_keys and self.key_file_name is in directory
        """
        users = self.get_users()
        if username in users:
            dir = os.path.join(self.path_to_keys, username)
            if self.key_file_name in os.listdir(dir):
                return True

        return False

    def deploy_key(self, user_names):
        """
        Finds public key in self.path_to_keys/username/self.key_file_name a create dir structure on filer:
          /vol/ROOT/etc/sshd/username/.ssh/authorized_keys2
        """
        users = []
        if isinstance(user_names, str):
            users = [user_names]
        else:
            users = user_names

        for user in users:
            pubkey = None
            path = join(self.path_to_keys, user, 'id_rsa.pub')
            try:
                file = open(path,'r')
                pubkey = file.read()
            except IOError as e:
                raise DeployKeyException("%s: %s" % (path, e.strerror))

            if pubkey:
                self._create_dir_structure(user)
                keys_path = posixpath.join('/vol', self.root_volume_name, 'etc', 'sshd', user,'.ssh', 'authorized_keys2')
                self.create_file(keys_path, pubkey)

        return True

    def delete_key(self, user_names):
        """
        Deletes authorized_keys2 file in /vol/ROOT/etc/sshd/username/.ssh/ and deletes .ssh and username dir
        """
        users = []
        if isinstance(user_names, str):
            users = [user_names]
        else:
            users = user_names

        for user in users:
            keys_path = posixpath.join('/vol', self.root_volume_name, 'etc', 'sshd', user,'.ssh', 'authorized_keys2')
            try:
                self.delete_file(keys_path)
            except deleteFileNotFoundException:
                pass

            ssh_dir_path = posixpath.join('/vol', self.root_volume_name, 'etc', 'sshd', user,'.ssh')
            user_dir_path = posixpath.join('/vol', self.root_volume_name, 'etc', 'sshd', user)
            try:
                self.delete_dir(ssh_dir_path)
                self.delete_dir(user_dir_path)
            except deleteDirNotFoundException:
                pass

        return True

