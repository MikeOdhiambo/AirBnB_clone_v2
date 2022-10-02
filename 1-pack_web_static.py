#!/usr/bin/python3
"""pack_web_static - Generates a .tgz archive of AirBnBclone"""


def do_pack():
    """Generates an archive and stores it in /versions with date-generated format"""
    local("mkdir -p versions/")
    check_cmd = local("tar -czf versions/web_static$(date +%Y%m%d%H%M%S).tgz web_static/")
    if check_cmd.failed:
        return None
    else:
        return local("ls -t versions/ | head -n1")
