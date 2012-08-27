# -*- coding: utf-8 -*-

from fabric.api import *


env.hosts = ['localhost']

env.dev_branch = 'dev'


def prepare_deploy():
    local('./manage.py test')
    local('git add -p && git commit')
    local('git push')