radamanth.mysql-ansible
=========

This Simple role install Mongodb without authentication, replica set or others things.

Requirements
------------

Target platform should be an ubuntu with apt-get capabilities

Role Variables
--------------

```yaml
#  MONGO PORT TO LISTEN
mongodb_port: 27017
# MONGO BIND IP, let this to localhost if you want some privacy
mongodb_bind_ip: 127.0.0.1

# System user where backup of the mongo dbs will be stored every day
mongodb_backup_user: "mongo-admin"
# Max number of backup to store on file system
mongodb_backup_max_days: 30


# What version do you want to install
mongodb_org_version : "3.0.5"
# By default every other package are on the same version
mongodb_org_server_version : "{{ mongodb_org_version}}"
mongodb_org_shell_version  : "{{ mongodb_org_version}}"
mongodb_org_mongos_version  : "{{ mongodb_org_version}}"
mongodb_org_tools_version  : "{{ mongodb_org_version}}"
```


Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: radamanth.mongo-ansible }

License
-------

GPLV2

Author Information
------------------
I've been a computer science engineer for more than 10 years now, I've discovered Ansible in 2014, and fell in love with it. I use it in my company to manage different server since then. Feel free to visit our site www.neovia.fr

I'm also one of the founder of Immozeo, where Ansible is also greatly used. ( www.immozeo.com)

