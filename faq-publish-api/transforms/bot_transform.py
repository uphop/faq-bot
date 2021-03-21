import os
import sys
from shutil import copyfile, copytree, rmtree
import logging
logger = logging.getLogger(__name__)

'''
Generates Rasa bot based on templates
'''
class BotTransform:
    def __init__(self, output_folder_prefix):
        self.output_folder_prefix = output_folder_prefix
        
    """
    Generates Rasa bot runtime based on a template and on provided user's input.
    """
    def transform(self):
        logger.debug('Generating bot replica.')
        bot_root_output_folder = self.delete_bot_output_folder(self.output_folder_prefix)
        bot_root_output_folder = self.prepare_bot_output_folder(self.output_folder_prefix)
        bot_output_folder = self.clone_bot_from_template(bot_root_output_folder)
        logger.debug('Bot replica ready at: ' + bot_output_folder)
        return bot_output_folder

    def prepare_bot_output_folder(self, output_folder_prefix):
        BROADCAST_OUTPUT_FOLDER = os.getenv('BROADCAST_OUTPUT_FOLDER', './output')
        bot_output_folder = BROADCAST_OUTPUT_FOLDER + '/' + output_folder_prefix
        os.makedirs(bot_output_folder)
        return bot_output_folder

    def delete_bot_output_folder(self, output_folder_prefix):
        BROADCAST_OUTPUT_FOLDER = os.getenv('BROADCAST_OUTPUT_FOLDER', './output')
        bot_output_folder = BROADCAST_OUTPUT_FOLDER + '/' + output_folder_prefix
        if os.path.exists(bot_output_folder):
            rmtree(bot_output_folder)
        return bot_output_folder

    def clone_bot_from_template(self, output_folder):
        # make a copy of Rasa bot
        BROADCAST_TEMPLATE_FOLDER = os.getenv('BROADCAST_TEMPLATE_FOLDER', './templates')
        BROADCAST_BOT_TEMPLATE_FOLDER = os.getenv('BROADCAST_BOT_TEMPLATE_FOLDER', 'bot')
        BROADCAST_BOT_OUTPUT_FOLDER = os.getenv('BROADCAST_BOT_OUTPUT_FOLDER', 'bot')

        bot_template_folder = BROADCAST_TEMPLATE_FOLDER + '/' + BROADCAST_BOT_TEMPLATE_FOLDER
        bot_output_folder = output_folder + '/' + BROADCAST_BOT_OUTPUT_FOLDER

        # make a copy of template broadcast folder
        try:
            copytree(bot_template_folder, bot_output_folder)
        except OSError as err:
            logger.error("Error: % s" % err)

        return bot_output_folder

    def cleanup(self):
        self.delete_bot_output_folder(self.output_folder_prefix)
