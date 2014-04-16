# Helper functions for docker

import docker
import os

DEFAULT_DOCKER_API_VERSION = '1.10'
BASEIMAGETAG = "glusterbase:latest"
GLUSTERIMAGENAME = "gluster:latest"
BASEDIR = os.getcwd()


class DockerHelper (docker.Client):
    """
    Extended docker client with some helper functions
    """
    def __init__(self):
        super(DockerHelper, self).__init__(version=DEFAULT_DOCKER_API_VERSION)

    def image_by_id(self, id):
        """
        Return image with given Id
        """
        if not id:
            return None
        return next((image for image in self.images() if image['Id'] == id),
                    None)

    def image_by_tag(self, tag):
        """
        Return image with given tag
        """
        if not tag:
            return None

        return next((image for image in self.images() if tag
                     in image['RepoTags']), None)

    def image_exists(self, id=None, tag=None):
        """
        Check if specified image exists
        """
        exists = False
        if id and self.image_by_id(id):
            exists = True
        elif tag and self.image_by_tag(tag):
            exists = True

        return exists

    def container_by_id(self, id):
        """
        Returns container with given id
        """
        if not id:
            return None
        return next((container for container in self.containers(all=True)
                     if container['Id'] == id), None)

    def container_by_name(self, name):
        """
        Returns container with given name
        """
        if not name:
            return None

        # docker prepends a '/' to container names in the container dict
        name = '/'+name
        return next((container for container in self.containers(all=True)
                     if name in container['Names']), None)

    def container_exists(self, id=None, name=None):
        """
        Checks if container exists already
        """
        exists = False
        if id and self.container_by_id(id):
            exists = True
        elif name and self.container_by_name(name):
            exists = True

        return exists

    def container_running(self, id=None, name=None):
        """
        Checks if container is running
        """
        running = False
        if id:
            running = self.inspect_container(id)['State']['Running']
        elif name:
            running = self.inspect_container(name)['State']['Running']
        return running

    def get_container_ip(self, container):
        """
        Returns the internal ip of the container if available
        """
        info = self.inspect_container(container)
        if not info:
            return None

        netInfo = info['NetworkSettings']
        if not netInfo:
            return None

        ip = netInfo['IPAddress']
        if not ip:
            return None

        return ip
