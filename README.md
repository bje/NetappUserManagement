# Distribution of users and public keys to Netapp storage boxes

## Overview

Modules and scripts to handle many users in Netapp filers environment.
It was not possible to use LDAP, because we need password-less logging in and LDAP doesnt support it on Netapps.
Therefore, I created scripts which can add/delete user/s on single or all filers in environment.

### How it works

This modules and scripts are useful in following cases:

1. Adding one or all users/keys to one filer or all filers in environment
2. Adding one or all users/keys from one filer or all filers in environment

All keys are stored in directory which is set in config file in variable `keypath`. Structure has to be following:

    /dir/to/keys/user_name/id_rsa.pub
    /dir/to/keys/user_name2/id_rsa.pub
    ...

List of filers is taken from `/etc/hosts` file or other file with appropriate syntax

### Requirements

* NetappSDK from my GitHub account (sudo pip install git+git://github.com/kmadac/NetappSDK.git)

### Installation

    sudo pip install git+git://github.com/kmadac/NetappUserManagement.git

Copy config file
    /opt/system/netapp_user_management/config_template.py
to
    /opt/system/netapp_user_management/config.py and adjust values for your environment.

### Configuration file variables

`keypath` - path to directory with the user public keys
`hosts_file` - path to hosts file
`hosts_filter` - list of strings which identifies line in hosts file which will be used for user management operations (most likely will start with #)
Example of such hosts file can be found in test directory.
`root_passwords` - list of root passwords which will be used by scripts to login to filer. Script will try one after another in case that logging in won't be successful. It was added because we have several different root passwords in environment.

### Usage examples

1. Add user **kmadac** to whole environment
    adduser_filer -u kmadac -af

2. Add all users to filer **NEW_FILER** (this filer have to be defined in `hosts` file)
    adduser_filer -au -f NEW_FILER

3. Remove user **kmadac** from the environment (at the moment it is part for **adduser_filer** script, but it'll be changed in near future)
    adduser_filer -d -u kmadac -af