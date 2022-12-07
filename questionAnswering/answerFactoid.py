# Question Answering Suite - Factoid Answering
# Tanay Bennur, Alexandra Knox, Kevin Ren

from setup import *
from extraction import *

""" Factoid Answering Functions """
def answer_question_bert(q, bow_doc, document, k):
  candidate_answers = []
  candidate_sentences = most_similar_sentence2(document, bow_doc , q, k)

  for s in candidate_sentences:
    candidate_answers.append(bert_answer({
      'question': q,
      'context': s
    }))
  
  # Find best answer from candidate list
  max_prob = 0
  best_answer = ""
  for c in candidate_answers:
    if c["score"] > max_prob:
      max_prob = c["score"]
      best_answer = c["answer"]
  
  return best_answer
