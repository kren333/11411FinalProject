# Question Answering Suite
# Tanay Bennur, Alexandra Knox, Kevin Ren


# imports
import sys
from setup import *
from extraction import *
from answerFactoid import *
from answerYesNo import *

# Question Answering Wrapper
def answer_question (q, embedding, document, k):
  if not(isYesNo(q)):
    a = answer_question_bert(q, embedding, document, k)  
  else:
    a = answer_Yes_No(q, embedding, document, k)
  return a

# Reads a txt file and creates a string
def read_file(file_name):
    file1 = open(file_name, "r")
    text = file1.read()
    file1.close()
    return text

# Main Function
def answer(articleFile, questionFile):
    data = read_file(questionFile)
    QUESTIONS = data.split('\n')

    ARTICLE = read_file(articleFile)
    embedding = bow(ARTICLE)

    for q in QUESTIONS:
        a = answer_question(q, embedding, ARTICLE, 6)
        print(a)

answer(sys.argv[1], sys.argv[2])
      

