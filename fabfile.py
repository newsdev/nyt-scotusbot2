import datetime
import json
import os

from fabric import api, operations, contrib
from fabric.state import env

ENVIRONMENTS = {
    "prd": {
        "hosts": 'ec2-23-21-126-6.compute-1.amazonaws.com',
    }, 
}

env.project_name = 'nyt-scotusbot2'
env.user = "ubuntu"
env.forward_agent = True
env.branch = "master"

env.hosts = ['127.0.0.1']
env.settings = None

@api.task
def development():
    env.branch = 'development'

@api.task
def master():
    env.branch = 'master'

@api.task
def branch(branch_name):
    env.branch = branch_name

@api.task
def e(environment):
    env.settings = environment
    env.hosts = ENVIRONMENTS[environment]['hosts']

@api.task
def clone():
    api.run('git clone git@github.com:newsdev/%(project_name)s.git /home/ubuntu/%(project_name)s' % env)

@api.task
def pull():
    api.run('cd /home/ubuntu/%(project_name)s; git fetch; git pull origin %(branch)s' % env)

@api.task
def pip_install():
    api.run('cd /home/ubuntu/%(project_name)s; workon %(project_name)s && pip install -r requirements.txt' % env)

@api.task
def mkvirtualenv():
    api.run('mkvirtualenv %(project_name)s' % env)

@api.task
def setup():
    clone()
    mkvirtualenv()
    pip_install()

@api.task
def deploy():
    pull()
    pip_install()

@api.task
def runbot():
    api.run('workon nyt-scotusbot2 && cd /home/ubuntu/nyt-scotusbot2 && ./bot.sh')

def killbot():
    api.sudo('killall scotusbot2')