# Question Generation Suite - Question Generation
# Tanay Bennur, Alexandra Knox, Kevin Ren


import math
import queue

from setup import *
from templating import *


""" Ranking Functions """
# Scores question via key entiteis present
def get_score(text, key_entities):
  total = 0
  for (entity, score) in key_entities:
    if entity in text:
      total += score
  return score * math.log(len(text.split(" ")))

""" Generation Functions """
# Finds score of question
def get_score(text, key_entities):
  total = 0
  for (entity, score) in key_entities:
    if entity in text:
      total += score
  return score * math.log(len(text.split(" ")))

# Generates all questions for a given sentence
def generate_sentence_questions(processed_text, key_entities, templates, escape_character, split_character, seperator_character):
  questions = []
  processed_text = nlp(processed_text.text)
  for template in templates:
    [text_template, question_template, score_multiplier, should_grammaticize] = template.split(seperator_character)
    if test_template(processed_text, text_template, split_character):
      entities = extract_entities(processed_text, text_template, split_character)
      question_text = merge_text(processed_text, question_template, escape_character, split_character, entities)
      question_score = float(score_multiplier) * get_score(question_text, key_entities)
      questions.append((question_text + chr(5) + should_grammaticize, question_score))
  return questions

# Reranks questions to include question template frequency
def frequency_rank_questions(questions):
  frequency_dict = {}
  final_queue = queue.PriorityQueue()
  while not questions.empty():
    score, question = questions.get()
    start_word = question.split()[0].lower()
    if start_word not in frequency_dict:
      frequency_dict[start_word] = 0
    frequency_dict[start_word] += 1
    final_queue.put((score * frequency_dict[start_word], question))
  return final_queue

# Generates all questions for given body of text
def generate_questions(sentences, key_entities, templates, escape_character, split_character, seperator_character, max_questions):
  questions = queue.PriorityQueue()
  for sentence in sentences:
    sentence_questions = generate_sentence_questions(sentence, key_entities, templates, escape_character, split_character, seperator_character)
    for question, score in sentence_questions:
      if questions.qsize() > max_questions:
        return frequency_rank_questions(questions)
      questions.put(((1 / score, question)))
  return frequency_rank_questions(questions)

""" Post Processing Functions """
# Grammaticizes and prints questions
def finalize_questions(questions, num_questions):
  questions_asked = 0
  prev_asked = None
  while questions_asked < int(num_questions) and not questions.empty():
    _, question = questions.get()
    input_sentence, should_grammaticize = question.split(chr(5))
    if input_sentence == prev_asked:
      continue
    prev_asked = input_sentence
    questions_asked += 1
    if (should_grammaticize == 'N'):
      print(input_sentence + "?")
      continue
    batch = tokenizer(input_sentence + "?", return_tensors='pt')
    generated_ids = model.generate(batch['input_ids'])
    generated_sentence = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    print(generated_sentence[0])
  if questions_asked < num_questions:
    print(f"Only {questions_asked} out of {num_questions} could be generated. Sorry about that!")
  else:
    print("All questions generated.")