import os
import sys
from shutil import copyfile, copytree, rmtree
import subprocess
import logging
logger = logging.getLogger(__name__)

'''
Trains Rasa bot
'''
class HotSwapTransform:
    def __init__(self, output_folder):
        self.output_folder = output_folder
    
    """
    Trains Rasa model within Broadcast bot replica
    """
    def transform(self, model_output_file):
        logger.debug('Broadcast model hot swap starting.')
        model_output_file = self.prepare_model_output_file(self.output_folder, model_output_file)
        logger.debug('Broadcast model hot swap finished.')
        return model_output_file

    def prepare_model_output_file(self, output_folder, model_output_file):
        BROADCAST_OUTPUT_FOLDER = os.getenv('BROADCAST_OUTPUT_FOLDER', './output')
        BROADCAST_OUTPUT_MODEL_FOLDER = os.getenv('BROADCAST_OUTPUT_MODEL_FOLDER', 'models')
        source_model_output_file_full_path = output_folder + '/' + BROADCAST_OUTPUT_MODEL_FOLDER + '/' + model_output_file
        target_model_output_file_full_path = BROADCAST_OUTPUT_FOLDER + '/' + model_output_file

        try:
            copyfile(source_model_output_file_full_path, target_model_output_file_full_path)
        except OSError as err:
            logger.error("Error: % s" % err)
        logger.debug('Copied model file.')

        return target_model_output_file_full_path

    
  