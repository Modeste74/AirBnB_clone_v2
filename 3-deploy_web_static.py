#!/usr/bin/python3
"""Deploy script for web_static project"""
from fabric.api import run, env, put, local
from datetime import datetime
from os.path import exists
from fabric.decorators import runs_once

env.hosts = ['54.90.0.245', '54.145.84.49']


def do_pack():
    """Packs the contents of web_static into a .tgz archive"""
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d%H%M%S")
    arch_f = "web_static_" + formatted_date + ".tgz"
    local("mkdir -p versions")
    result = local("tar -czvf versions/{} web_static".format(arch_f))
    if result.failed:
        return None
    return "versions/" + arch_f


def do_deploy(archive_path):
    """
    Distributes an archive to web servers

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory on web server
        archive_name = archive_path.split('/')[-1]
        put(archive_path, f'/tmp/{archive_name}')
        archive_no_ext = archive_name.split('.')[0]

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
    except Exception as e:
        print(e)
        return False


@runs_once
def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
