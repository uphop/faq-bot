import os
import sys
from shutil import copyfile, copytree, rmtree
import subprocess
import logging
logger = logging.getLogger(__name__)

'''
Trains Rasa bot
'''
class ModelTransform:
    def __init__(self, output_folder):
        self.output_folder = output_folder
    
    """
    Trains Rasa model within Broadcast bot replica
    """
    def transform(self, model_file_prefix):
        logger.debug('Broadcast bot training starting.')
        model_output_file = self.train_model(self.output_folder, model_file_prefix)
        logger.debug('Trained broadcast bot model: ' + model_output_file)
        return model_output_file
    
    def train_model(self, output_folder, model_file_prefix):
        # prepare Rasa training command
        model_train_command = [
            "rasa",
            "train",
            "--force",
            "--verbose",
            "--debug",
            "--fixed-model-name",
            model_file_prefix
        ]

        # create a subprocess for rasa train command, setting current working directory to the broadcast's directory
        process = subprocess.Popen(model_train_command,
                                   cwd=output_folder,
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True
                                   )

        # run broadcast bot training
        while True:
            output = process.stdout.readline()
            logger.info(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                # Process has finished, read rest of the output
                for output in process.stdout.readlines():
                    logger.info(output.strip())
                    logger.info('Broadcast bot training completed.')
                break

        model_output_file = model_file_prefix + '.tar.gz'
        return model_output_file