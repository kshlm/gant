#! /usr/bin/env python2

from docopt import docopt
from .utils.gant_docker import GantDocker
import os

helpStr = """
Gant : The Gluster helper ant
Creates GlusterFS development and testing environments using Docker

Usage:
    gant [options] build-base [force]
    gant [options] build-main <srcdir>[force]
    gant [options] launch <number>
    gant [options] stop [<name>] [force]
    gant [options] info
    gant [options] ssh <name>

Commands:
    build-base  Builds the base docker image
    build-main  Builds the main docker image to be used for launching containers
    launch      Launches the given number of containers
    stop        Stops the launched containers
    info        Gives information about the gant environment
    ssh         SSHes into the named container

Arguments:
    force     Forcefully do the operation
    <srcdir>  Directory containing the GlusterFS source
    <number>  Number of containers to launch
    <name>    Name of container to stop

Options:
    -c <conffile>, --conf <conffile>  Configuration file to use
    --basetag <basetag>               Tag to be used for the base docker image [default: glusterbase:latest]
    --maintag <maintag>               Tag to be used for the main docker image [default: gluster:latest]
    --basedir <basedir>               Base directory containing the Dockerfile and helper scripts for Gant [default: {0}]
    --prefix <prefix>                 Prefix to be used for naming the launched docker containers [default: gluster]
""".format(os.getcwd())

def main():
    args = docopt(helpStr, version = "Gant v0.0.1")
    g = GantDocker()

    if args["build-base"]:
        g.build_base_image (args)
    elif args["build-main"]:
        g.build_main_image (args)
    elif args["launch"]:
        g.launch(args)
    elif args["stop"]:
        g.stop(args)
    elif args["info"]:
        g.info(args)
    elif args["ssh"]:
        g.ssh(args)
