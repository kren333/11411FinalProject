# Question Generation Suite - Term Extraction and Sentence Ranking
# Tanay Bennur, Alexandra Knox, Kevin Ren

import wordfreq
import queue

from setup import *

""" Sentence Parsing Functions """
# Checks if a given pattern matches a document fragment
def check_pattern(doc, i, pattern):
  for index, types in pattern:
    if i + index < 0 or i + index >= len(doc):
      return False
    if not (doc[i + index].tag_ in types):
      return False
  return True

# Check if document fragment is legal
def should_continue(doc, i, patterns):
  for pattern in patterns:
    if check_pattern(doc, i, pattern):
      return True
  return False

# Checks that a document fragment is english
def all_valid(phrase, banned_chars):
  for token in phrase:
    if not token.isascii():
      return False
    for char in banned_chars:
      if char in token:
        return False
  return True

""" Document Scanning Functions """
# Uses heuristic to normalize by overall word frequency
def normalize_doc_count(doc_count, smoothing_factor, normalize_function):
  for phrase in doc_count:
    score = 0
    for token in phrase.split(" "):
      score += (wordfreq.zipf_frequency(token, 'en') + smoothing_factor)
    doc_count[phrase] /= normalize_function(score)

# Iterates through doc to extract phrases
def process_file(doc, patterns, banned_chars, smoothing_factor, normalize_function, min_word_len):
  doc_count = {}
  i = 0

  while i < len(doc):
    phrase = []
    while should_continue(doc, i, patterns):
      phrase.append(doc[i].text)
      i += 1
    if phrase != [] and all_valid(phrase, banned_chars):
      noun = " ".join(phrase).lower()
      if len(noun) >= min_word_len:
        if not (noun in doc_count):
          doc_count[noun] = 0
        doc_count[noun] += 1
    i += 1

  normalize_doc_count(doc_count, smoothing_factor, normalize_function)
  return list(sorted(doc_count.items(), key = lambda x: x[1]))

""" Sentence Clustering Functions """
# Scans document to identify sentences with a lot of key phrases
def sentence_priority(doc, key_phrases, max_term = -1):
  sentences_queue = queue.PriorityQueue()
  phrases = (key_phrases[::-1])[:max_term]
  for sent in doc.sents:
    score = 0
    for (word, value) in phrases:
      if word in sent.text.lower():
        score += value
      score /= max(1, len(sent.text.split()))
    sentences_queue.put((1/(score + 0.00001), sent))
  return sentences_queue

# Non-destructively returns top results
def return_top_x_sentences(sentences_queue, x):
  top_sentences = []
  temp =  queue.PriorityQueue()
  for _ in range(x):
    if sentences_queue.empty(): break
    (score, sent) = sentences_queue.get()
    temp.put((score, sent))
    top_sentences.append(sent)
  for _ in range(x):
    if temp.empty(): break
    (score, sent) = temp.get()
    sentences_queue.put((score, sent))
  return top_sentences