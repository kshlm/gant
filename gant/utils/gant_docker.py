from __future__ import unicode_literals

import os
import grp
import time
import json

from click import echo

from .docker_helper import DockerHelper
from . import ssh


def check_permissions():
    """
    Checks if current user can access docker
    """
    if (
        not grp.getgrnam('docker').gr_gid in os.getgroups()
        and not os.geteuid() == 0
    ):
        exitStr = """
        User doesn't have permission to use docker.
        You can do either of the following,
        1. Add user to the 'docker' group (preferred)
        2. Run command as superuser using either 'sudo' or 'su -c'
        """
        exit(exitStr)


class GantDocker (DockerHelper):
    """
    Gluster test env specific helper functions for docker
    """
    def __init__(self):
        super(GantDocker, self).__init__()

    def setConf(self, conf):
        self.conf = conf

    def __handle_build_stream(self, stream, verbose):
        for line in stream:
            d = json.loads(line.decode('utf-8'))
            if "error" in d:
                return d["error"].strip()
            elif verbose:
                echo(d["stream"].strip())
        return None

    def build_base_image_cmd(self, force):
        """
        Build the glusterbase image
        """
        check_permissions()

        basetag = self.conf.basetag
        basedir = self.conf.basedir
        verbose = self.conf.verbose

        if self.image_exists(tag=basetag):
            if not force:
                echo("Image with tag '{0}' already exists".format(basetag))
                return self.image_by_tag(basetag)
            else:
                self.remove_image(basetag)
        echo("Building base image")
        stream = self.build(path=basedir, rm=True, tag=basetag)
        err = self.__handle_build_stream(stream, verbose)
        if err:
            echo("Building base image failed with following error:")
            echo(err)
            return None

        image = self.image_by_tag(basetag)
        echo("Built base image {0} (Id: {1})".format(basetag, image['Id']))
        return image

    def build_main_image_cmd(self, srcdir, force):
        """
        Build the main image to be used for launching containers
        """
        check_permissions()

        basetag = self.conf.basetag
        basedir = self.conf.basedir
        maintag = self.conf.maintag

        if not self.image_exists(tag=basetag):
            if not force:
                exit("Base image with tag {0} does not exist".format(basetag))
            else:
                echo("FORCE given. Forcefully building the base image.")
                self.build_base_image_cmd(force)

        if self.image_exists(tag=maintag):
            self.remove_image(tag=maintag)

        build_command = "/build/make-install-gluster.sh"
        container = self.create_container(image=basetag, command=build_command,
                                          volumes=["/build", "/src"])

        self.start(container, binds={basedir: "/build", srcdir: "/src"})
        echo('Building main image')
        while self.inspect_container(container)["State"]["Running"]:
            time.sleep(5)

        if not self.inspect_container(container)["State"]["ExitCode"] == 0:
            echo("Build failed")
            echo("Dumping logs")
            echo(self.logs(container))
            exit()

        # The docker remote api expects the repository and tag to be seperate
        # items for commit
        repo = maintag.split(':')[0]
        tag = maintag.split(':')[1]
        image = self.commit(container['Id'], repository=repo, tag=tag)
        echo("Built main image {0} (Id: {1})".format(maintag, image['Id']))

    def launch_cmd(self, n, force):
        """
        Launch the specified docker containers using the main image
        """
        check_permissions()

        prefix = self.conf.prefix
        maintag = self.conf.maintag

        commandStr = "supervisord -c /etc/supervisor/conf.d/supervisord.conf"
        createDevFuse = "mknod /dev/fuse c 10 229"

        for i in range(1, n+1):
            cName = "{0}-{1}".format(prefix, i)

            if self.container_exists(name=cName):
                if not force:
                    exit("Container with name {0} already "
                         "exists.".format(cName))
                else:
                    if self.container_running(name=cName):
                        self.stop(cName)
                    self.remove_container(cName, v=True)

            c = self.create_container(image=maintag, name=cName,
                                      command=commandStr, volumes=["/bricks"])
            self.start(c['Id'], privileged=True)
            time.sleep(2)  # Wait for container to startup

            ssh.do_cmd('root', self.get_container_ip(c['Id']), 'password',
                       createDevFuse)

            echo("Launched {0} (Id: {1})".format(cName, c['Id']))
            c = None
            cName = None

    def stop_cmd(self, name, force):
        """
        Stop the specified or all docker containers launched by us
        """
        check_permissions()

        if name:
            echo("Would stop container {0}".format(name))
        else:
            echo("Would stop all containers")
        echo("For now use 'docker stop' to stop the containers")

    def info_cmd(self, args):
        """
        Print information on the built up environment
        """
        echo('Would print info on the gluster env')

    def ssh_cmd(self, name, ssh_command):
        """
        SSH into given container and executre command if given
        """
        if not self.container_exists(name=name):
            exit("Unknown container {0}".format(name))

        if not self.container_running(name=name):
            exit("Container {0} is not running".format(name))

        ip = self.get_container_ip(name)
        if not ip:
            exit("Failed to get network address for "
                 "container {0}".format(name))
        if ssh_command:
            ssh.do_cmd('root', ip, 'password', " ".join(ssh_command))
        else:
            ssh.launch_shell('root', ip, 'password')

    def ip_cmd(self, name):
        """
        Print ip of given container
        """
        if not self.container_exists(name=name):
            exit('Unknown container {0}'.format(name))

        ip = self.get_container_ip(name)
        if not ip:
            exit("Failed to get network address for"
                 " container {0}".format(name))
        else:
            echo(ip)

    def gluster_cmd(self, args):
        name = args["<name>"]
        ssh_command = args["<gluster-command>"]

        if not self.container_exists(name=name):
            exit("Unknown container {0}".format(name))

        if not self.container_running(name=name):
            exit("Container {0} is not running".format(name))

        ip = self.get_container_ip(name)
        if not ip:
            exit("Failed to get network address for"
                 " container {0}".format(name))
        if ssh_command:
            ssh.do_cmd('root', ip, 'password',
                       "gluster {0}".format(" ".join(ssh_command)))
        else:
            ssh.do_cmd('root', ip, 'password', 'gluster')
