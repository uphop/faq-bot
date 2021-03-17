import os
import sys
import ruamel
import ruamel.yaml
from ruamel.yaml.scalarstring import PreservedScalarString as pss
from shutil import copyfile, copytree, rmtree
import logging
logger = logging.getLogger(__name__)

'''
Generates Rasa NLU based on template
'''
class NLUTransform:
    def __init__(self, output_folder):
        self.output_folder = output_folder
        
    """
    Generates Rasa NLU based on a template and on provided user's input.
    """
    def transform(self, items):
        logger.debug('Generating NLU training data.')

        # make a copy of NLU template
        nlu_output_file = self.prepare_nlu_output_file(self.output_folder)

        # init YAML
        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = False

        # open copied template and load YAML
        with open(nlu_output_file, 'r') as stream:
            documents = yaml.load(stream)

        # add current basket items to the end of the YAML document
        logger.debug('Enriching template with variations.')
        for item in items:
            # prepare a new intent element
            faq_intent = self.get_faq_intent(item)

            # add intent to the doc
            documents['nlu'].append(faq_intent)

        # save intents back to the output YAML file
        logger.debug('Saving NLU training data.')
        with open(nlu_output_file, 'w') as file:
            yaml.dump(documents, file)

        # return output file path
        return nlu_output_file

    def prepare_nlu_output_file(self, output_folder):
        # make a copy of NLU template
        BROADCAST_TEMPLATE_FOLDER = os.getenv('BROADCAST_TEMPLATE_FOLDER', './templates')
        BROADCAST_TEMPLATE_NLU_FILE = os.getenv('BROADCAST_TEMPLATE_NLU_FILE', 'nlu.yml')
        BROADCAST_OUTPUT_NLU_FILE = os.getenv('BROADCAST_OUTPUT_NLU_FILE', 'nlu.yml')

        nlu_template_file = BROADCAST_TEMPLATE_FOLDER + '/' + BROADCAST_TEMPLATE_NLU_FILE
        nlu_output_file = output_folder + '/' + BROADCAST_OUTPUT_NLU_FILE

        try:
            copyfile(nlu_template_file, nlu_output_file)
        except OSError as err:
            logger.error("Error: % s" % err)
        logger.debug('Copied NLU template.')

        return nlu_output_file

    def get_faq_intent(self, item):
        # add original question
        examples = '- ' + item['question'] + '\n'

        # concatenate question variations
        for question_variation in item['question_variations']:
            examples += '- ' + question_variation + '\n'

        # prepare a new intent element
        faq_intent = {
            'intent': 'faq/' + item['topic_id'],
            'examples': pss(examples)
        }

        return faq_intent