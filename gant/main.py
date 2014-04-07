#! /usr/bin/env python2

from docopt import docopt
from .utils.gant_docker import GantDocker

helpStr = """
Gant : The Gluster helper ant
Creates GlusterFS development and testing environments using Docker

Usage:
    gant [options] build-base [force]
    gant [options] build-main [force]
    gant [options] launch <number>
    gant [options] stop [<name>] [force]
    gant [options] info
    gant [options] ssh <name>

Options:
    -c <conffile>, --conf <conffile>  Configuration file to use
    --base-tag <basetag>              Tag to be used for the base docker image [default: glusterbase:latest]
    --main-tag <maintag>              Tag to be used for the main docker image [default: gluster:latest]
    --prefix <prefix>                 Prefix to be used for naming the launched docker containers [default: gluster]

Arguments:
    force   Forcefully do the operation
    number  Number of containers to launch
    name    Name of container to stop
"""


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

