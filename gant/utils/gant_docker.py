from docker_helper import DockerHelper

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
        if self.image_exists(tag = BASEIMAGETAG):
            if not args["force"]:
                print "Image with tag '%s' already exists"%(BASEIMAGETAG)
                return  self.image_by_tag (BASEIMAGETAG)
            else:
                self.remove_image (BASEIMAGETAG)

        self.build(path = BASEDIR, rm = True, tag = BASEIMAGETAG)

    def build_main_image (self, args):
        print "Would build the main image"

    def launch (self, args):
        print "Would launch %s containers using the main image"%(args["number"])

    def stop (self, args):
        if args["name"]:
            print "Would stop container %s"%(args["name"])
        else:
            print "Would stop all containers"

    def info (self, args):
        print 'Would print info on the gluster env'

    def ssh (self, args):
        print 'Would ssh into container %s'%(args['name'])
