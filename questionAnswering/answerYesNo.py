# Question Answering Suite - Yes/No Answering
# Tanay Bennur, Alexandra Knox, Kevin Ren


import spacy
from setup import *
from extraction import *


""" Yes/No Answering Functions """
# Parses Yes/No Question
def parse_question(question):
  q = nlp(question)

  #course, slightly hard-coded way to extract important words
  query = []
  for token in q:
    allowed_pos = {"ADJ", "ADV", "NOUN", "NUM", "PROPN", "SYM", "VERB"}
    if (token.pos_ in allowed_pos):
      query.append(token.text)
  return " ".join(query)

# Answers Yes/No Question
def answer_Yes_No (q, bow_doc, document, k):
  candidate_answers = []
  candidate_sentences = most_similar_sentence2(document, bow_doc , q, k)

  #find imporant words (nouns, adjectives, etc.) from the question
  words_in_query = parse_question(q).split()

  for s in candidate_sentences:
    
    all_words = True
    for w in words_in_query:
      if not (w in s):
        all_words = False
    if all_words:
      candidate_answers.append("Yes")
    else:
      answer = yn_answer({
        'text': s,
        'text_pair': q
      })

      if (answer["label"] == "LABEL_0" and answer["score"] > 0.80):
        candidate_answers.append("Yes")
      else:
        candidate_answers.append("No")
      
  if "Yes" in candidate_answers:
    return "Yes"
  else:
    return "No"