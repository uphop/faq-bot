import os
import sys
import random
import docker
import logging

logger = logging.getLogger(__name__)

'''
Buils and starts Rasa bot runtime.
'''
class RuntimeTransform:
    def __init__(self, output_folder):
        # save output folder
        self.output_folder = output_folder

        # init Docker daemon
        base_url = os.getenv('BROADCAST_DOCKER_HOST_BASE_URL', 'unix://var/run/docker.sock')
        self.client = docker.APIClient(base_url=base_url)
        
    """
    Builds and launches broadcast bot Docker image
    """
    def transform(self, user_id, spot_id):
        logger.debug('Broadcast runtime is starting.')
        
        # get image tag
        tag = os.getenv('BROADCAST_IMAGE_OWNER', 'unhop') + '/' + user_id

        # delete any previoulsy started containers for that image
        self.drop_containers(tag)

        # delete any previoulsy built images with the same name
        self.drop_images(tag)

        # create new Docker image based on Rasa base image and trained bot model
        self.create_image(tag, self.output_folder)

        # create a new container based on that image
        container_id, container_ip_addr_external, container_port_external = self.create_container(tag, spot_id)

        # start that container
        self.launch_container(tag, container_id)
        
        logger.debug('Broadcast runtime is ready.')

        # prepare broadcast URL
        broadcast_url = 'http://' + container_ip_addr_external + ':' + str(container_port_external)
        # broadcast_url = os.getenv('BROADCAST_CONTAINER_BASE_URL', 'http://localhost')+ ':' + str(broadcast_container_port_external)
        return broadcast_url

    def drop_images(self, tag):
        logger.debug('Deleting image: ' + tag)
        # get list of all images
        images = self.client.images(all=True)

        # iterate through images, filter by tag, and delete found ones
        for image in images:
            for repo_tag in image['RepoTags']:
                if repo_tag.startswith(tag):
                    self.client.remove_image(image=image['Id'], force=True, noprune=False)

    def create_image(self, tag, path):
        logger.debug('Creating new image: ' + tag)

        # build new image
        build_result = self.client.build(path=path, tag=tag, rm=True)
        response = [line for line in build_result]
        logger.debug(response)

    def drop_containers(self, tag):
        logger.debug('Deleting containers for image: ' + tag)

        # filter containers by image tag
        filters = {'ancestor': tag}
        containers = self.client.containers(all=True, filters=filters)

        # force stop and delete all found containers
        for container in containers:
            self.client.remove_container(container=container['Id'], v=True, force=True)
    
    def create_container(self, tag, spot_id):
        logger.debug('Creating container for image: ' + tag)

        # prepare port config
        BROADCAST_CONTAINER_PORT_INTERNAL = int(os.getenv('BROADCAST_CONTAINER_PORT_INTERNAL', '5005'))
        BROADCAST_CONTAINER_PORT_RANGE_START = int(os.getenv('BROADCAST_CONTAINER_PORT_RANGE_START', '5010'))
        BROADCAST_CONTAINER_PORT_RANGE_END = int(os.getenv('BROADCAST_CONTAINER_PORT_RANGE_END', '7010'))
        broadcast_container_port_external = BROADCAST_CONTAINER_PORT_RANGE_START + spot_id
        ports = [BROADCAST_CONTAINER_PORT_INTERNAL]
        port_bindings={BROADCAST_CONTAINER_PORT_INTERNAL: broadcast_container_port_external}
        
        # build container
        image = tag + ':latest'
        host_config = self.client.create_host_config(port_bindings=port_bindings, auto_remove=True)
        container = self.client.create_container(image=image, detach=True, ports=ports, host_config=host_config)
        broadcast_container_ip_addr_external = container.attrs['NetworkSettings']['IPAddress']
        
        print(broadcast_container_port_external)
        return container.get('Id'), broadcast_container_ip_addr_external, broadcast_container_port_external
        
    def launch_container(self, tag, container_id):
        logger.debug('Launching container for image: ' + tag)

        # start container
        self.client.start(container=container_id)


    
  