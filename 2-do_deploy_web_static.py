#!/usr/bin/python3
"""Distributes an archive to web servers"""
from fabric.api import env, put, run
import os

env.hosts = ['54.90.0.245', '54.145.84.49']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory on web server
        archive_name = os.path.basename(archive_path)
        put(archive_path, '/tmp/{}'.format(archive_name))
        archive_no_ext = os.path.splitext(archive_name)[0]

        # Create the release folder
        release_folder = '/data/web_static/releases/' + archive_no_ext
        run('mkdir -p {}'.format(release_folder))

        # Uncompress the archive to release folder
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, release_folder))

        # Delete the uploaded archive
        run('rm /tmp/{}'.format(archive_name))

        # Move contents from release folder to current folder
        run('mv {}/web_static/* {}'.format(release_folder, release_folder))

        # Remove the empty web_static folder
        run('rm -rf {}/web_static'.format(release_folder))

        # Delete the old current link
        run('rm -rf /data/web_static/current')

        # Create a new symlink
        run('ln -s {} /data/web_static/current'.format(release_folder))
        return True
    except Exception:
        return False
