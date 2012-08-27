# -*- coding: utf-8 -*-

from fabric.api import *

env = env
env.hosts = ['localhost']

env.dev_branch = 'dev'
env.master_branch = 'master'

def commit():
    local('git commit -a')

def merge():
    local('git checkout %s' % env.master_branch)
    local('git merge --no-ff %s' % env.dev_branch)


def push():
    commit()
    merge()
    local('git push')
    local('git checkout %s' % env.dev_branch)
