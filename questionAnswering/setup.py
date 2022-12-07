# Question Answering Suite - Setup
# Tanay Bennur, Alexandra Knox, Kevin Ren

import spacy
from spacy.language import Language
from transformers import BertForQuestionAnswering, AutoTokenizer
from transformers import pipeline
from transformers import BertForSequenceClassification

# Custom Sentencizer Setup
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
model = BertForQuestionAnswering.from_pretrained('../models/model_load')
tokenizer = AutoTokenizer.from_pretrained('../models/tokenizer_qa_load')
bert_answer = pipeline('question-answering', model=model, tokenizer=tokenizer)
yn_model = BertForSequenceClassification.from_pretrained('../models/yn_model')
yn_answer = pipeline('text-classification', model=yn_model, tokenizer=tokenizer)

""" Hyperparameters """
NOUN_WEIGHT = 2
UNIGRAM_WEIGHT = 1
BOOL_INDICATORS = {"be", "do", "have"}
