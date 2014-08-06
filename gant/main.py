#! /usr/bin/env python

from __future__ import unicode_literals, print_function

from .utils.gant_ctx import GantCtx

import os
import click

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
    -V, --verbose                     Verbose output
""".format(os.getcwd())


@click.group(no_args_is_help=True)
@click.option("-c", "--conf", type=click.File(),
              help="Configuration file to use")
@click.option("--basedir", default=os.getcwd(),
              type=click.Path(exists=True, file_okay=False, readable=True),
              help="Directory containing the Dockerfile and helper scripts "
              "for GAnt")
@click.option("--basetag", default="glusterbase:latest", show_default=True,
              help="Tag to be used for the base docker image")
@click.option("--maintag", default="gluster:latest", show_default=True,
              help="Tag to be used for the main docker image")
@click.option("--prefix", default="gluster", show_default=True,
              help="Prefix used for naming launched containers")
@click.option("--verbose", "-v", count=True, metavar="",
              help="Increase verbosity of output")
@click.version_option(prog_name='GAnt')
@click.pass_context
def gant(ctx, conf, basedir, basetag, maintag, prefix, verbose):
    """
    GAnt : The Gluster helper ant\n
    Creates GlusterFS development and testing environments using Docker
    """
    ctx.obj.initConf(basetag, maintag, basedir, prefix, verbose)
    ctx.obj.gd.setConf(ctx.obj.conf)


@gant.command(name="build-base", help="Build the base docker image")
@click.option("--force", is_flag=True, default=False,
              help="Forcefully do the operation")
@click.pass_context
def build_base(ctx, force):
    ctx.obj.gd.build_base_image_cmd(force)


@gant.command(name="build-main",
              help="Build the main docker image to be used for launching")
@click.option("--force", is_flag=True, default=False,
              help="Forcefully do the operation")
@click.argument("srcdir",
                type=click.Path(exists=True, file_okay=False, readable=True))
@click.pass_context
def build_main(ctx, srcdir, force):
    ctx.obj.gd.build_main_image_cmd(srcdir, force)


@gant.command(help="Launch the given number of containers")
@click.option("--force", is_flag=True, default=False,
              help="Forcefully do the operation")
@click.argument("number", type=click.INT)
@click.pass_context
def launch(ctx, number, force):
    ctx.obj.gd.launch_cmd(number, force)


@gant.command(help="Stop the launched containers")
@click.option("--force", is_flag=True, default=False,
              help="Forcefully do the operation")
@click.argument("name", required=False, type=click.STRING)
@click.pass_context
def stop(ctx, name, force):
    ctx.obj.gd.stop_cmd(name, force)


@gant.command(help="Show information about the GAnt environment")
@click.pass_context
def info(ctx):
    ctx.obj.gd.info_cmd()


@gant.command(help="Print ip of given container")
@click.argument("container", type=click.STRING)
@click.pass_context
def ip(ctx, container):
    ctx.obj.gd.ip_cmd(container)


@gant.command(help="SSHes into named container and runs command if given")
@click.argument("container", type=click.STRING)
@click.argument("command", required=False, type=click.STRING, nargs=-1)
@click.pass_context
def ssh(ctx, container, command):
    ctx.obj.gd.ssh_cmd(container, command)


@gant.command(help="Runs given gluster command in named container")
@click.argument("container", type=click.STRING)
@click.argument("command", type=click.STRING, nargs=-1)
def gluster(ctx, container, command):
    ctx.obj.gd.gluster_cmd(container, command)


def main():
    gant(obj=GantCtx())
