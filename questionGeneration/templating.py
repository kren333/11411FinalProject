# Question Generation Suite - Template Functions
# Tanay Bennur, Alexandra Knox, Kevin Ren


""" Term Extraction Functions """
# Tests if a template can be applied to a specific body of text
def test_template(text, template, split_character):
  match_list = [tuple(token.split(split_character)) for token in template.split()]
  token_list = [token for token in text]
  i = 0
  j = 0
  while j < len(token_list) and i < len(match_list):
    (match_type, match_val) = match_list[i]
    if match_type == 'G':
      if token_list[j].tag_ == match_val:
        i += 1
        j += 1
      else:
        if i == 0:
          j += 1
        else:
          return False
    elif match_type == 'E':
      if token_list[j].ent_type == 0:
        j += 1
      elif token_list[j].ent_type_ != match_val:
        return False
      else:
        while j < len(token_list) and token_list[j].ent_type_ == match_val:
          j += 1
        i += 1
    elif match_type == 'R':
      return True
  return (i == len(match_list))

# Given applicable template, extracts key entities
def extract_entities(text, template, split_character):
  entities = {}
  match_list = [tuple(token.split(split_character)) for token in template.split()]
  token_list = [token for token in text]
  [head] = list(filter(lambda x: x == x.head, token_list))
  i = 0
  j = 0
  while j < len(token_list) and i < len(match_list):
    (match_type, match_val) = match_list[i]
    if match_type == 'G':
      entities[match_val] = token_list[j]
      i += 1
      j += 1
    elif match_type == 'E':
      if token_list[j].ent_type == 0:
        j += 1
      else:
        ent = token_list[j]
        while j < len(token_list) and token_list[j].ent_type_ == match_val:
          j += 1
        while ent.head != head:
          ent = ent.head
        entities[match_val] = ent
        i += 1
    elif match_type == 'R':
      s = []
      while j < len(token_list) and (token_list[j].text.isalnum() or token_list[j].text != "."):
        s.append(token_list[j].text)
        j += 1
      i += 1
      entities["REST"] = " ".join(s)
  return entities


""" Template Merging Functions """
# Finds token in greater body of text
def get_text(processed_text, token, tag, full, get_first):
  all_text = []
  text_list = [token for token in processed_text]
  scan_on = False
  i = 0
  while i < len(text_list):
    if text_list[i] == token:
      scan_on = True
      j = 0
      while i >= 0 and text_list[i].ent_type_ == tag:
        all_text.insert(0, text_list[i].text)
        i -= 1
        j += 1
      i += j
    elif (text_list[i].ent_type_ == tag and get_first):
      all_text.insert(0, text_list[i].text)
      break
    elif scan_on:
      if text_list[i].ent_type_ == tag:
        all_text.append(text_list[i].text)
        j = i + 1
        while j < len(text_list):
          if text_list[j].ent_type_ == tag:
            all_text.append(text_list[j].text)
          else:
            break
          j += 1
        if i - 1 >= 0 and (str(text_list[i - 1].tag_) == "NNP" or str(text_list[i - 1].tag_) == "DT"):
          all_text.insert(0, text_list[i - 1].text)
      elif text_list[i].text != "," and str(text_list[i].tag_) != "NNP":
        scan_on = False
        break
    i += 1
  if full:
    return token.text + " " + " ".join(all_text)
  return " ".join(all_text)

# Merges template with text entities from processed text
def merge_text(processed_text, template, escape_character, split_character, entities):
  template_list = template.split()
  for i in range(len(template_list)):
    item = template_list[i]
    if item[0] == escape_character:
      [tag, option] = item[1:].split(split_character)
      if option[0] == "E":
        template_list[i] = get_text(processed_text, entities[tag], tag, True, False) + option[1:]
      if option[0] == "F":
        template_list[i] = get_text(processed_text, entities[tag], tag, False, True) + option[1:]
      elif option[0] == "N":
        template_list[i] = get_text(processed_text, entities[tag], tag, False, False) + option[1:]
      elif option[0] == "L":
        template_list[i] = entities[tag].lemma_ + option[1:]
      elif option[0] == "R":
        template_list[i] = entities[tag] + option[1:]
      else:
        template_list[i] = entities[tag].text + option[1:]
  return " ".join(template_list)
