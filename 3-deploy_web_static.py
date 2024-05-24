#!/usr/bin/python3
""" Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers """

import time
from fabric.api import local, put, env, run
from os.path import exists, isdir
env.hosts = ['54.160.86.192', '54.160.113.163']


def do_pack():
    """ A function that generates a .tgz archive """
    try:
        file_name = "versions/web_static_{}.tgz".format(
            time.strftime("%Y%m%d%H%M%S"))
        if isdir("versions") is False:
            local("mkdir versions")
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """ A function that distributes an archive to your web servers """
    try:
        if exists(archive_path):
            file_name = archive_path.split("/")[-1]
            file_no_ext = file_name.split(".")[0]
            path = "/data/web_static/releases/"
            put(archive_path, "/tmp/")
            run('mkdir -p {}{}/'.format(path, file_no_ext))
            run('tar -xzf /tmp/{} -C {}{}/'.format(
                file_name, path, file_no_ext))
            run('rm /tmp/{}'.format(file_name))
            run('mv {0}{1}/web_static/* {0}{1}/'.format(
                path, file_no_ext))
            run('rm -rf {}{}/web_static'.format(path, file_no_ext))
            run('rm -rf /data/web_static/current')
            run('ln -fs {}{}/ /data/web_static/current'.format(
                path, file_no_ext))
            return True
        else:
            return False
    except Exception:
        return False


def do_deploy_local(archive_path):
    """ A function that distributes an archive to your local machine """
    try:
        if exists(archive_path):
            file_name = archive_path.split("/")[-1]
            file_no_ext = file_name.split(".")[0]
            path = "/data/web_static/releases/"
            local("cp {} /tmp/".format(archive_path))
            local('mkdir -p {}{}/'.format(path, file_no_ext))
            local('tar -xzf /tmp/{} -C {}{}/'.format(
                file_name, path, file_no_ext))
            local('rm /tmp/{}'.format(file_name))
            local('mv {0}{1}/web_static/* {0}{1}/'.format(
                path, file_no_ext))
            local('rm -rf {}{}/web_static'.format(path, file_no_ext))
            local('rm -rf /data/web_static/current')
            local('ln -fs {}{}/ /data/web_static/current'.format(
                path, file_no_ext))
            return True
        else:
            return False
    except Exception:
        return False


def deploy():
    """ A function that distributes an archive to your web servers """
    # if env.hosts == ['54.160.86.192', '54.160.113.163']:
    #     return do_deploy(do_pack())
    # else:
    return do_deploy_local(do_pack())
