import os
import grp
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
        bsaedir = args["--basedir"]
        if self.image_exists(tag = basetag):
            if not args["force"]:
                print "Image with tag '%s' already exists"%(basetag)
                return  self.image_by_tag (basetag)
            else:
                self.remove_image (basetag)

        self.build(path = basedir, rm = True, tag = basedir)

    def build_main_image (self, args):
        """
        Build the main image to be used for launching containers
        """
        check_permissions()

        print "Would build the main image"

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
