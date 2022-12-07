# Question Generation Suite
# Tanay Bennur, Alexandra Knox, Kevin Ren

# Imports
import sys
import csv

from setup import *
from extraction import *
from templating import *
from generation import *

""" File Management Functions """
# Converts template tsv to folder
def read_tsv(file_name):
  templates = []
  with open(file_name) as file:
    tsv_file = csv.reader(file, delimiter="\t")     
    for line in tsv_file:
        templates.append(":".join(line))
  return templates

# Reads a txt file and creates a string
def read_file(file_name):
  file1 = open(file_name, "r")
  text = file1.read()
  file1.close()
  return text

# Main Function
def ask(filename, num_questions):
  # Preprocessing
  text = read_file(filename)
  templates = read_tsv("question_generation_templates.tsv")
  doc = nlp(text)

  # Extraction
  key_phrases = process_file(doc, LEGAL_PATTERNS, BANNED_CHARACTERS, FREQ_SMOOTH, NORMALIZE_SCORE, MIN_WORD_LENGTH)
  sentences_queue = sentence_priority(doc, key_phrases, MAX_PRIORITY_TERMS)
  candidate_sentences = return_top_x_sentences(sentences_queue, NUM_SENTENCES)

  # Generation
  questions = generate_questions(candidate_sentences, key_phrases, templates, ESCAPE_CHARACTER, SPLIT_CHARACTER, SEPERATOR_CHARACTER, MAX_QUESTIONS)
  finalize_questions(questions, num_questions)

ask(sys.argv[1], sys.argv[2])