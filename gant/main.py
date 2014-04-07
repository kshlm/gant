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
    force                             Forcefully do the operation
    number                            Number of containers to launch

"""


def main():
    args = docopt(helpStr, version = "Gant v0.0.1")
