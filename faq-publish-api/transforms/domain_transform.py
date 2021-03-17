import os
import sys
import ruamel
import ruamel.yaml
from ruamel.yaml.scalarstring import PreservedScalarString as pss
from shutil import copyfile, copytree, rmtree
import logging
logger = logging.getLogger(__name__)

'''
Generates Rasa domain based on template
'''
class DomainTransform:
    def __init__(self, output_folder):
        self.output_folder = output_folder

    """
    Generates Rasa domain based on a template and on provided user's input.
    """
    def transform(self, items):
        # init YAML
        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = False

        domain_output_file = self.prepare_domain_output_file(self.output_folder)

        # open copied template and load YAML
        with open(domain_output_file, 'r') as stream:
            documents = yaml.load(stream)

        # add current basket items to the responses section of the YAML document
        for item in items:
            # prepare a new intent element
            intent, text = self.get_faq_intent(item)

            # add response to the doc
            documents['responses'][intent] = text

        # save intents back to the output YAML file
        with open(domain_output_file, 'w') as file:
            yaml.dump(documents, file)

        # return output file path
        return domain_output_file

    def prepare_domain_output_file(self, output_folder):
        # make a copy of domain template
        BROADCAST_TEMPLATE_FOLDER = os.getenv('BROADCAST_TEMPLATE_FOLDER', './templates')
        BROADCAST_TEMPLATE_DOMAIN_FILE = os.getenv('BROADCAST_TEMPLATE_DOMAIN_FILE', 'domain.yml')
        BROADCAST_OUTPUT_DOMAIN_FILE = os.getenv('BROADCAST_OUTPUT_DOMAIN_FILE', 'domain.yml')

        domain_template_file = BROADCAST_TEMPLATE_FOLDER + '/' + BROADCAST_TEMPLATE_DOMAIN_FILE
        domain_output_file = output_folder + '/' + BROADCAST_OUTPUT_DOMAIN_FILE
        
        try:
            copyfile(domain_template_file, domain_output_file)
        except OSError as err:
            logger.error("Error: % s" % err)

        return domain_output_file

    def get_faq_intent(self, item):
        # prepare a new intent element
        intent = 'utter_faq/' + item['topic_id']
        text = [{'text': item['answer']}]
        return intent, text