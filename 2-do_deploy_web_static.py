#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers
"""
from fabric.operations import local, run, put
from datetime import datetime
from fabric.api import env
import os
import re

env.hosts = ['104.196.55.234', '35.229.108.9']
env.user = "ubuntu"


def do_pack():
    """archives the web_static folder
    """
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    command = local("tar -czvf versions/web_static_{}.tgz web_static"
                    .format(time))
    if command.failed:
        return None
    else:
        return command


def do_deploy(archive_path):
    """ deploys web_static.tgz to the web servers
    """
    if not os.path.exists(archive_path):
        return False

    result = put(archive_path, "/tmp")
    if result.failed:
        return False

    rex = r'^versions/(\S+).tgz'
    match = re.search(rex, archive_path)
    filename = match.group(1)
    result = put(archive_path, "/tmp/{}.tgz".format(filename))
    if result.failed:
        return False
    result = run("mkdir -p /data/web_static/releases/{}/".format(filename))
    if result.failed:
        return False
    result = run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
                 .format(filename, filename))
    if result.failed:
        return False
    result = run("rm /tmp/{}.tgz".format(filename))
    if result.failed:
        return False
    result = run("mv /data/web_static/releases/{}"
                 "/web_static/* /data/web_static/releases/{}/"
                 .format(filename, filename))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/releases/{}/web_static"
                 .format(filename))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/current")
    if result.failed:
        return False
    result = run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
                 .format(filename))
    if result.failed:
        return False

    print('New version deployed!')

    return True
