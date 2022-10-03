#!/usr/bin/python3
"""do_deploy_web_static - Deploys a new web version to server"""

from fabric.operations import local, run, put
from fabric.api import env
import os
import re


env.hosts = ['18.232.52.18', '3.94.129.25']
env.user = 'ubuntu'


def do_pack():
    """
    Generates an archive and stores it in /versions with date-generated format
    """

    local("mkdir -p versions/")
    cmd = local("""
    tar -czf versions/web_static$(date +%Y%m%d%H%M%S).tgz web_static/
    """)
    if cmd.failed:
        return None
    else:
        return local("ls -t versions/ | head -n1")


def do_deploy(archive_path):
    """Send, uncompress and link new web files to server"""
    if not os.path.exists(archive_path):
        return False
    rex = r'^versions/(\S+).tgz'
    match = re.search(rex, archive_path)
    filename = match.group(1)
    res = put(archive_path, "/tmp/{}.tgz".format(filename))
    if res.failed:
        return False
    res = run("mkdir -p /data/web_static/releases/{}/".format(filename))
    if res.failed:
        return False
    res = run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
              .format(filename, filename))
    if res.failed:
        return False
    res = run("rm /tmp/{}.tgz".format(filename))
    if res.failed:
        return False
    res = run("mv /data/web_static/releases/{}"
              "/web_static/* /data/web_static/releases/{}/"
              .format(filename, filename))
    if res.failed:
        return False
    res = run("rm -rf /data/web_static/releases/{}/web_static"
              .format(filename))
    if res.failed:
        return False
    res = run("rm -rf /data/web_static/current")
    if res.failed:
        return False
    res = run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
              .format(filename))
    if res.failed:
        return False
    print('New version deployed!')
    return True
