from docker_helper import DockerHelper

class GantDocker (DockerHelper):
    """
    Gluster test env specific helper functions for docker
    """
    def __init__ (self):
        super (GantDocker, self).__init__()

    def build_base_image (self, force = False):
        """
        Build the glusterbase image
        """
        if self.image_exists(tag = BASEIMAGETAG):
            if not force:
                return  self.image_by_tag (BASEIMAGETAG)
            else:
                self.remove_image (BASEIMAGETAG)

        self.build(path = BASEDIR, rm = True, tag = BASEIMAGETAG)
