#! /usr/bin/env python

from docopt import docopt
from .utils.gant_docker import GantDocker
import os

helpStr = """
Gant : The Gluster helper ant
Creates GlusterFS development and testing environments using Docker

Usage:
    gant [options] build-base [force]
    gant [options] build-main <srcdir>[force]
    gant [options] launch <number> [force]
    gant [options] stop [<name>] [force]
    gant [options] info
    gant [options] ssh <name> [--] [<ssh-command>...]
    gant [options] ip <name>
    gant [options] gluster <name> [--] [<gluster-command>...]

Commands:
    build-base  Builds the base docker image
    build-main  Builds the main docker image to be used for launching
                containers
    launch      Launches the given number of containers
    stop        Stops the launched containers
    info        Gives information about the gant environment
    ssh         SSHes into the named container and runs the command if given
    ip          Gives IP address of the named container
    gluster     Runs given gluster CLI command in named container

Arguments:
    force              Forcefully do the operation
    <srcdir>           Directory containing the GlusterFS source
    <number>           Number of containers to launch
    <name>             Name of container to stop
    <ssh-command>      Command to run inside the container
    <gluster-command>  Gluster CLI command to run inside the container

Options:
    -c <conffile>, --conf <conffile>  Configuration file to use
    --basetag <basetag>               Tag to be used for the base docker image
                                      [default: glusterbase:latest]
    --maintag <maintag>               Tag to be used for the main docker image
                                      [default: gluster:latest]
    --basedir <basedir>               Base directory containing the Dockerfile
                                      and helper scripts for Gant
                                      [default: {0}]
    --prefix <prefix>                 Prefix to be used for naming the
                                      launched docker containers
                                      [default: gluster]
""".format(os.getcwd())


def main():
    args = docopt(helpStr, version="Gant v0.0.6")
    g = GantDocker()

    if args["build-base"]:
        g.build_base_image_cmd(args)
    elif args["build-main"]:
        g.build_main_image_cmd(args)
    elif args["launch"]:
        g.launch_cmd(args)
    elif args["stop"]:
        g.stop_cmd(args)
    elif args["info"]:
        g.info_cmd(args)
    elif args["ssh"]:
        g.ssh_cmd(args)
    elif args["ip"]:
        g.ip_cmd(args)
    elif args["gluster"]:
        g.gluster_cmd(args)
