# Question Generation Suite - Setup and Hyperparameters
# Tanay Bennur, Alexandra Knox, Kevin Ren


import spacy
from spacy.language import Language
from transformers import BartForConditionalGeneration, BartTokenizer


""" Model Setup """
# Sentencizer Setup
@Language.component("custom_sentencizer_addon")
def set_custom_sentence_end_points(doc):
    for token in doc[:-1]:
        if token.text == '\n':
            doc[token.i+1].is_sent_start = True
        elif token.text == '\r':
            doc[token.i+1].is_sent_start = True
        elif token.text == '=':
            doc[token.i+1].is_sent_start = True
    return doc

# Model Loading
nlp = spacy.load('../models/nlp_model/')
model = BartForConditionalGeneration.from_pretrained('../models/paraphrase_model')
tokenizer = BartTokenizer.from_pretrained('../models/tokenizer_model')

""" Magic Symbol Setup """
LEGAL_PATTERNS = [[(0, ["NN", "NNP", "NNS"])],
                  [(0, ["JJ"]), (1, ["NN", "NNP", "NNS"])],
                  [(-1, ["NN", "NNP", "NNS"]), (0, ["IN"]), (1, ["NN", "NNP", "NNS"])]]

BANNED_CHARACTERS = ["=", "!", "@", "%"]
ESCAPE_CHARACTER = "@"
SPLIT_CHARACTER = "-"
SEPERATOR_CHARACTER = ":"

""" Hyperparameter Control """
FREQ_SMOOTH = 0.9
LENGTH_WEIGHT = 0.4

MAX_PRIORITY_TERMS = 150
NUM_SENTENCES = 150
MIN_WORD_LENGTH = 4
MAX_QUESTIONS = 80

def NORMALIZE_SCORE(score):
  return score ** LENGTH_WEIGHT
