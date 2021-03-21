import os
import sys
import random
import docker
import time
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
    def transform(self, user_id, spot_id, broadcast_name):
        logger.debug('Broadcast runtime is starting.')
        
        # get image tag
        tag = os.getenv('BROADCAST_IMAGE_OWNER', 'unhop') + '/' + user_id

        # delete any previoulsy started containers for that image
        self.drop_containers(tag)

        # create new Docker image based on Rasa base image and trained bot model
        self.create_image(tag, self.output_folder)

        # create a new container based on that image, and launch it
        broadcast_url = self.create_container(tag, spot_id, broadcast_name)
        
        logger.debug('Broadcast runtime is ready, listening on: ' + broadcast_url)
        return broadcast_url

    def drop_containers(self, tag):
        logger.debug('Deleting containers for image: ' + tag)

        # filter containers by image tag
        filters = {'ancestor': tag}
        containers = self.client.containers(all=True, filters=filters)

        # force stop and delete all found containers
        for container in containers:
            self.client.remove_container(container=container['Id'], v=True, force=True)

    def create_image(self, tag, path):
        logger.debug('Creating new image: ' + tag)

        # build new image
        build_result = self.client.build(path=path, rm=True, forcerm=True, tag=tag, nocache=True, pull=True)
        response = [line for line in build_result]
        logger.debug(response)

        #clean-up old builds
        self.client.prune_builds()

        # clean-up old images
        self.client.prune_images()
        self.client.prune_volumes()

    def create_container(self, tag, spot_id, broadcast_name):
        logger.debug('Creating container for image: ' + tag)

        # prepare networking config
        BROADCAST_CONTAINER_PORT_INTERNAL = int(os.getenv('BROADCAST_CONTAINER_PORT_INTERNAL', '5005'))
        BROADCAST_CONTAINER_PORT_RANGE_START = int(os.getenv('BROADCAST_CONTAINER_PORT_RANGE_START', '5010'))
        BROADCAST_CONTAINER_NETWORK_MODE = os.getenv('BROADCAST_CONTAINER_NETWORK_MODE', 'faq-bot_default')

        broadcast_container_port_external = BROADCAST_CONTAINER_PORT_RANGE_START + spot_id
        port_bindings={BROADCAST_CONTAINER_PORT_INTERNAL: broadcast_container_port_external}
        ports = [BROADCAST_CONTAINER_PORT_INTERNAL]

        host_config = self.client.create_host_config(network_mode=BROADCAST_CONTAINER_NETWORK_MODE, port_bindings=port_bindings)
        networking_config = self.client.create_networking_config({BROADCAST_CONTAINER_NETWORK_MODE: self.client.create_endpoint_config()})
        
        # build container
        container = self.client.create_container(image=tag, name=broadcast_name, detach=True, ports=ports, host_config=host_config, networking_config=networking_config)

        # start container
        self.client.start(container=container.get('Id'))

        # wait for container to become ready
        container_ip = ''
        BROADCAST_CONTAINER_MAX_START_ATTEMPTS = int(os.getenv('BROADCAST_CONTAINER_MAX_START_ATTEMPTS', '10'))
        current_start_attempts = 0

        while True:
            # check if already waited for too long, and if so - return an empty IP
            current_start_attempts += 1
            if current_start_attempts > BROADCAST_CONTAINER_MAX_START_ATTEMPTS:
                logger.error('Cannot get network details of container: ' + container.get('Id'))
                break

            time.sleep(.500)

            # try to get container IP and port
            container_details = self.client.inspect_container(container.get('Id'))
            container_networks = container_details['NetworkSettings']['Networks']
            bot_network = container_networks.get(BROADCAST_CONTAINER_NETWORK_MODE)
            if not bot_network is None:
                container_ip = bot_network['IPAddress']
                if not container_ip is None and len(container_ip) > 0:
                    break
        
        broadcast_url = 'http://' + container_ip + ':' + str(BROADCAST_CONTAINER_PORT_INTERNAL)
        return broadcast_url