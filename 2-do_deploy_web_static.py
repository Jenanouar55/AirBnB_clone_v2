#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
import os

env.hosts = ['3.89.155.80', '54.237.29.246']


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        print("Archive path does not exist")
        return False
    try:
        file_n = os.path.basename(archive_path)
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        tmp_path = '/tmp/'

        # Upload the archive to /tmp/
        put(archive_path, tmp_path)

        # Create the release directory
        run('mkdir -p {}{}/'.format(path, no_ext))

        # Unpack the archive
        run('tar -xzf {}{} -C {}{}/'.format(tmp_path, file_n, path, no_ext))

        # Remove the archive from /tmp/
        run('rm {}'.format(tmp_path + file_n))

        # Move the files
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))

        # Remove the current symlink and create a new one
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))

        return True
    except Exception as e:
        print(f"Error during deployment: {e}")
        return False
