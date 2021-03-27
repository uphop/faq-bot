import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
import logging
logger = logging.getLogger(__name__)

'''
Updates Rasa NLU examples with synonims.
'''
class SynonimTransform:
    def __init__(self):
        # nltk init
        NLTK_DATA_FOLDER = os.getenv('NLTK_DATA_FOLDER', './nltk_data')
        nltk.download('stopwords', download_dir=NLTK_DATA_FOLDER)
        nltk.download('punkt', download_dir=NLTK_DATA_FOLDER)
        nltk.download('averaged_perceptron_tagger', download_dir=NLTK_DATA_FOLDER)
        nltk.download('wordnet', download_dir=NLTK_DATA_FOLDER)
        nltk.data.path.append(NLTK_DATA_FOLDER)

        self.supported_tags = ['JJ', 'JJR', 'JJS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

    """
    Generates variations of user's questions by enriching with synonims.
    """
    def transform(self, items):
        logger.debug('Started synonim enrichment.')

        # go through all faq examples and tokenze each question
        for item in items:
            # enrich original example with question variations
            item['question_variations'] = self.get_question_variations(item['question'])
        
        logger.debug('Completed synonim enrichment.')
        return items

    def get_question_variations(self, question):
        # go through tokenized and tagged words and get synonims for nounds and verbs
        tagged_word_list = self.get_tagged_word_list(question)
        word_variations = self.get_word_variations(tagged_word_list)

        # generate variations of questions using word synonims
        question_variations = self.generate_question_variations(question, word_variations)
        
        # make list unique, and drop the original question, if there is such
        question_variations = list(set(question_variations))
        if question in question_variations:
            question_variations.remove(question)

        # slice question variations to limit those
        MAX_SYNONIMS = int(os.getenv('MAX_SYNONIMS', '5'))
        question_variations = question_variations[:MAX_SYNONIMS]

        return question_variations

    def generate_question_variations(self, question, word_variations):
        # get current word
        word = next(iter(word_variations))

        # go through variations of the current word, and create question variations
        question_variations = []
        for word_variation in word_variations[word]:
            question_variation = question.replace(word, word_variation)
            question_variations.append(question_variation)

            # check if this is the last word variation
            if len(word_variations) > 1:
                # if not yet, let's go deeper into recursion
                next_word_variations = dict(word_variations)
                # delete the current word
                next_word_variations.pop(word, None)
                # pass word variations down
                next_question_variations = self.generate_question_variations(question_variation, next_word_variations)
                # add recursively returned variations to the current result
                question_variations.extend(next_question_variations)
       
        return question_variations

    def get_word_variations(self, tagged_word_list):
        # go through tokenized and tagged words and get synonims for nounds and verbs
        variations = {}
        for tagged_word in tagged_word_list:
            word = tagged_word[0]
            tag = tagged_word[1]

            # check if the tag is supported
            if not tag in self.supported_tags:
                continue

            # get synonims for the word
            variations[word] = self.get_synonims(word)
            
        return variations

    def get_synonims(self, word):
        # go through each synonim
        synonims = []
        for synset in wordnet.synsets(word): 
            for lemma in synset.lemmas():
                # add synonim to the result
                synonim = lemma.name()
                synonim = synonim.replace('_', ' ')
                synonims.append(synonim)
        
        return synonims
    
    def get_tagged_word_list(self, question):
        # Word tokenizers is used to find the words and punctuation in a string
        tokenized_word_list = nltk.word_tokenize(question)

        # removing stop words from wordList
        stop_words = set(stopwords.words('english'))
        tokenized_word_list_non_stop = [
            w for w in tokenized_word_list if not w in stop_words]

        # Using a Tagger. Which is part-of-speech tagger or POS-tagger.
        tagged_word_list = nltk.pos_tag(tokenized_word_list_non_stop)
        return tagged_word_list
