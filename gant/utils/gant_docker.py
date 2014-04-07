import os
import grp
import time
from docker_helper import DockerHelper

def check_permissions():
    """
    Checks if current user can access docker
    """
    if not grp.getgrnam('docker').gr_gid in os.getgroups() and not os.geteuid() == 0:
        exitStr = """
        User doesn't have permission to use docker. You can do either of the following,
        1. Add user to the 'docker' group (preferred)
        2. Run command as superuser using either 'sudo' or 'su -c'
        """
        exit (exitStr)

class GantDocker (DockerHelper):
    """
    Gluster test env specific helper functions for docker
    """
    def __init__ (self):
        super (GantDocker, self).__init__()

    def build_base_image (self, args):
        """
        Build the glusterbase image
        """
        check_permissions()

        basetag = args["--basetag"]
        basedir = args["--basedir"]
        force   = args["force"]

        if self.image_exists(tag = basetag):
            if not force:
                print "Image with tag '%s' already exists"%(basetag)
                return  self.image_by_tag (basetag)
            else:
                self.remove_image (basetag)
        print "Building base image"
        image = self.build(path = basedir, rm = True, tag = basetag)
        print "Built base image {0} (Id: {1})".format()

    def build_main_image (self, args):
        """
        Build the main image to be used for launching containers
        """
        check_permissions()

        basetag = args["--basetag"]
        basedir = args["--basedir"]
        maintag = args["--maintag"]
        srcdir  = args["<srcdir>"]
        force   = args["force"]

        if not self.image_exists(tag = basetag):
            if not force:
                exit ("Base image with tag {0} does not exist".format(basetag))
            else:
                print "FORCE given. Forcefully building the base image."
                self.build_base_image(args)

        if self.image_exists(tag = maintag):
            self.remove_image(tag = maintag)

        build_command = "/build/make-install-gluster.sh"
        container = self.create_container(image = basetag, command = build_command, volumes = ["/build", "/src"])

        self.start (container, binds = {basedir : "/build", srcdir : "/src"})
        print 'Building main image'
        while self.inspect_container(container)["State"]["Running"]:
            time.sleep(5)

        if not self.inspect_container(container)["State"]["ExitCode"] == 0:
            print "Build failed"
            print "Dumping logs"
            print self.logs(container)
            exit()

        # The docker remote api expects the repository and tag to be seperate items for commit
        repo = maintag.split(':')[0]
        tag = maintag.split(':')[1]
        image = self.commit(container['Id'], repository = repo, tag = tag)
        print "Built main image {0} (Id: {1})".format(maintag, image['Id'])

    def launch (self, args):
        """
        Launch the specified docker containers using the main image
        """
        check_permissions()

        print "Would launch %s containers using the main image"%(args["number"])

    def stop (self, args):
        """
        Stop the specified or all docker containers launched by us
        """
        check_permissions()

        if args["name"]:
            print "Would stop container %s"%(args["name"])
        else:
            print "Would stop all containers"

    def info (self, args):
        """
        Print information on the built up environment
        """
        print 'Would print info on the gluster env'

    def ssh (self, args):
        print 'Would ssh into container %s'%(args['name'])
