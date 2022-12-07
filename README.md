# Overview
This is the source code behind a two-part question system \
The question generation module generates questions via ask.py \
The question answering module answer questions via answer.py \
These modules use a neural models from huggingface as well as custom statistics and tagging functions to achieve their tasks.

# Question Generation
This module generates n questions from text file t.txt \
It can be run via ./questionGeneration/ask.py t.txt n \
Our model uses a template-based approach with SPACY that searches through relevant sentences in a given document after preprocessing text, attempting to identify sequences of words that match certain human-generated templates after sentencization and part of speech (POS) and NER tagging.

# Question Answering
This module uses a.txt to answer the questions in b.txt \
It can be run via ./questionAnswering/answer.py a.txt b.txt \
Our model uses an IR-based approach to QA: we will identify the top few sentences within a document that are most likely to contain the answer and extract candidate answers from each sentence, ultimately returning our most confident answer.
