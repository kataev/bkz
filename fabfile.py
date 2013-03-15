# -*- coding: utf-8 -*-

from fabric.api import *
import fabtools

env.roledefs['production'] = ['bkz@server']

env.dev_branch = 'dev'
env.master_branch = 'master'

def commit():
    local('git commit -a')

def merge():
    local('git checkout %s' % env.master_branch)
    local('git merge %s' % env.dev_branch)
    local('git checkout %s' % env.dev_branch)

def push():
    merge()
    local('git push')
    local('git checkout %s' % env.dev_branch)

def dbstart():
    local('sudo service postgresql start')

def production_env():
	env.user = 'bkz'
	env.python = '~/env/bin/python'
	env.project_root = '~/bkz'

@roles('production')
def restart():
	sudo('supervisorctl restart bkz',shell=False)

@roles('production')
def deploy():
	production_env()
	with cd(env.project_root):
		run('git fetch')
		run('git merge origin/master')
		with fabtools.python.virtualenv('/home/bkz/env'):
			run('./manage.py collectstatic --noinput')
			run('./manage.py migrate --noinput')
	sudo('supervisorctl restart bkz',shell=False)