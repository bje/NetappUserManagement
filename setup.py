from distutils.core import setup
from distutils import dir_util

dir_util.mkpath('/opt/system/netapp_user_management')

setup(
    name='NetappUserManagement',
    version='0.3',
    packages=['UserManagement'],
    scripts=['bin/adduser_filer'],
    data_files=[('/opt/system/netapp_user_management', ['bin/config.py'])],
    url='',
    license='',
    author='kmadac',
    author_email='kamil.madac@t-systems.sk',
    description='Netapp User Management Suite'
)
