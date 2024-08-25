#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to the web servers.

Usage:
    fab -f 3-deploy_web_static.py deploy -i <path_to_ssh_private_key> -u <username>
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
import os

# Define the hosts (web servers)
env.hosts = ['<3.89.155.80>', '<54.237.29.246>']

def do_pack():
    """Generates a tgz archive."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print(f"Error creating archive: {e}")
        return None

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        print("Archive path does not exist")
        return False
    try:
        file_name = os.path.basename(archive_path)
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        
        # Upload the archive to the server
        put(archive_path, '/tmp/')
        
        # Create the directory on the server
        run('mkdir -p {}{}/'.format(path, no_ext))
        
        # Extract the archive to the new directory
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ext))
        
        # Remove the archive from the server
        run('rm /tmp/{}'.format(file_name))
        
        # Move the contents of web_static to the new release directory
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        
        # Remove the web_static directory
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        
        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')
        
        # Create a new symbolic link to the new release
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        
        return True
    except Exception as e:
        print(f"Error deploying archive: {e}")
        return False

def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
