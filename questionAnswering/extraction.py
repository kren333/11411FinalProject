# Question Answering Suite - Extraction and Parsing
# Tanay Bennur, Alexandra Knox, Kevin Ren

import spacy
import heapq
from setup import *

""" Extraction Functions """
# Creates bag of words model of document
def bow(document):
  vocab = {}
  nouns = nlp(document)
  words = document.split()
  for noun_chunk in nouns.noun_chunks:
    try:
      vocab[(noun_chunk.text).lower()] += 1
    except KeyError:
      vocab.update({(noun_chunk.text).lower() : 1})
  for w in words:
    try:
      vocab[w.lower()] += 1
    except KeyError:
      vocab.update({w.lower() : 1})
  return vocab

# Finds most similar sentences
def most_similar_sentence2(document, bow_doc, question, k): 
  q = nlp(question)
  noun_chunks = set()
  for noun_chunk in q.noun_chunks:
    noun_chunks.add(noun_chunk.text)
  words_in_question = set(question.split())
  
  doc = nlp(document)
  sentences = set()
  for s in doc.sents:
    sentences.add(str(s))

  sim_scores = {}

  for s in sentences:
    sim_score = 0
    sent = nlp(s)
    for n in sent.noun_chunks:
      nc = n.text
      if nc in noun_chunks:
        sim_score += NOUN_WEIGHT * (1/bow_doc[nc.lower()])
    
    words_in_sentence = set(s.split())
    for w in words_in_question:
      if w in words_in_sentence:
        sim_score += UNIGRAM_WEIGHT * (1/bow_doc[w.lower()])

    sim_scores.update({s : sim_score})

  return heapq.nlargest(k, sim_scores, key=sim_scores.get)

""" Parsing Functions """
# Determines if question is Yes/No
def isYesNo(question) :
  q = nlp(question)
  for token in q:
    firstLemma = token.lemma_
    isModalVerb = token.dep_ == 'aux' and token.tag_ == 'MD'
    break
  decision = (firstLemma in BOOL_INDICATORS) or isModalVerb

  if ", " in question:
    q = nlp(question.split(", ", 1) [1])
    for token in q:
      firstLemma = token.lemma_
      isModalVerb = token.dep_ == 'aux' and token.tag_ == 'MD'
      break
    decision = decision or (firstLemma in BOOL_INDICATORS) or isModalVerb

  if (" or " in question) and (firstLemma in BOOL_INDICATORS):
    decision = False

  return decision