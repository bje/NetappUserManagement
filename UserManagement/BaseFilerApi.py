from NetappSDK.NaServer import NaServer
from NetappSDK.NaElement import NaElement

__author__ = 'kmadac'

class ApiNotEnabledException(Exception): pass

class FileException(Exception): pass
class deleteFileNotFoundException(Exception): pass

class AuthorizationFailed(Exception): pass

class createUserException(Exception): pass
class createUserAlreadyExistsException(Exception): pass
class deleteUserException(Exception): pass
class deleteUserNotFoundException(Exception): pass
class listUsersException(Exception): pass


class DirException(Exception): pass
class deleteDirNotFoundException(Exception): pass
class createDirException(Exception): pass


class BaseFilerApi(object):
    def __init__(self, filer, login, password):
        self.filer = filer
        self.login = login
        self.api_major = 1
        self.api_minor = 4

        self.naserver = NaServer(self.filer, self.api_major, self.api_minor)
        self.naserver.set_server_type("FILER")
        self.naserver.set_transport_type("HTTP")
        self.naserver.set_port(80)
        self.naserver.set_style("LOGIN")

        if isinstance(password, str):
            self.naserver.set_admin_user(self.login, password)
            if not self.test_authorization():
                raise AuthorizationFailed
        elif isinstance(password, list):
            found = False
            for onepass in password:
                self.naserver.set_admin_user(self.login, onepass)
                if self.test_authorization():
                    found = True
                    break
            if not found:
                raise AuthorizationFailed

    def test_authorization(self):
        api = NaElement("system-get-version")
        xo = self.naserver.invoke_elem(api)
        if xo.results_status() == "failed":
            if xo.results_errno() == 13002:
                return False

        return True

    def create_file(self, path, data):
        datahex = data.encode("hex")

        api = NaElement("file-write-file")
        api.child_add_string("data", datahex)
        api.child_add_string("offset", "0")
        api.child_add_string("path", path)

        xo = self.naserver.invoke_elem(api)
        if xo.results_status() == "failed":
            raise FileException(xo.results_errno(), xo.results_reason())

    def delete_file(self, path):
        api = NaElement("file-delete-file")
        api.child_add_string("path", path)

        xo = self.naserver.invoke_elem(api)
        if xo.results_status() == "failed":
            if xo.results_errno() == '2':
                raise deleteFileNotFoundException(xo.results_errno(), xo.results_reason())
            elif xo.results_errno() == 13001:
                    raise ApiNotEnabledException(xo.results_errno(), xo.results_reason())
            else:
                raise FileException(xo.results_errno(), xo.results_reason())

        return True

    def create_dir(self, path, perm='755'):
        """
        Create directory specified by path. Assumes that only last dir in path needs to be created and preceeding
         dirs in path already exists.
        If directory exists or was created, it will return path
        In case of any error it will raise createDirException
        """
        api = NaElement("file-create-directory")
        api.child_add_string("path", path)
        api.child_add_string("perm", perm)

        xo = self.naserver.invoke_elem(api)
        if xo.results_status() == "failed":
            if xo.results_errno() == '17':
                #if directory exists it means, that dir is created and returns True
                return path
            else:
                raise createDirException(xo.results_errno(), xo.results_reason())

        return path

    def delete_dir(self, path):
        api = NaElement("file-delete-directory")
        api.child_add_string("path", path)

        xo = self.naserver.invoke_elem(api)
        if xo.results_status() == "failed":
            if xo.results_errno() == '2':
                raise deleteDirNotFoundException(xo.results_errno(), xo.results_reason())
            else:
                raise DirException(xo.results_errno(), xo.results_reason())

        return True

    def delete_user(self, login_name):
        api = NaElement("useradmin-user-delete")
        api.child_add_string("user-name", login_name)

        xo = self.naserver.invoke_elem(api)
        if xo.results_status() == "failed":
            if xo.results_errno() == '13114':
                raise deleteUserNotFoundException(xo.results_errno(), xo.results_reason())
            else:
                raise deleteUserException(xo.results_errno(), xo.results_reason())

        return True

    def list_users(self):
        """
        Returns list of strings of user names: [u'administrator', u'cifs_adm', u'netappsupport']
        """
        users = []
        api = NaElement("useradmin-user-list")

        xo = self.naserver.invoke_elem(api)

        if xo.results_status() == "failed":
            raise listUsersException(xo.results_reason())

        for user in xo.child_get('useradmin-users').children_get():
            users.append(user.child_get_string('name'))

        return users

    def create_user(self, login_name, password, full_name=''):
        """
        Create user by API (same as useradmin user add in CLI)
        """

        api = NaElement("useradmin-user-add")
        api.child_add_string("password", password)

        xi = NaElement("useradmin-user")
        api.child_add(xi)

        xi1 = NaElement("useradmin-user-info")
        xi.child_add(xi1)

        xi1.child_add_string("comment", "UserManagement")
        xi1.child_add_string("full-name", full_name)
        xi1.child_add_string("name", login_name)

        xi2 = NaElement("useradmin-groups")
        xi1.child_add(xi2)

        xi3 = NaElement("useradmin-group-info")
        xi2.child_add(xi3)

        xi3.child_add_string("name", "Administrators")

        xo = self.naserver.invoke_elem(api)
        if xo.results_status() == "failed":
            if xo.results_errno() == '13114':
                raise createUserAlreadyExistsException(xo.results_errno(), xo.results_reason())
            elif xo.results_errno() == 13001:
                raise ApiNotEnabledException(xo.results_errno(), xo.results_reason())
            elif xo.results_errno() == 13002:
                raise AuthorizationFailed(xo.results_errno(), xo.results_reason())
            else:
                raise createUserException(xo.results_errno(), xo.results_reason())

        return True
