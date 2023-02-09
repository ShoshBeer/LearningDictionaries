import json

lst = []
releventKeys = ["word", "pos", "lang_code"]
with open("kaikki.org-dictionary-English-most-senses-10.json", "r", encoding="utf-8") as f:
    for line in f: 
      data = json.loads(line)
      if ' ' in data["word"]:
        #skip multi-word phrases
        pass
      elif data["pos"] not in "noun verb adj adv":
        #only take nouns, verbs, adjectives, and adverbs
        pass
      elif data["senses"][0].get("raw_glosses") == None:
        #idk what this takes out, the senses array has "raw_glosses" and "glosses" and they look like the same thing and seem like definitions
        #for some reason, some don't have "raw_glosses" so this just prevents an error when grabbing the definition
        #later I can look through the ones without it and check what's being skipped and if the definition is stored elsewhere
        pass
      elif "obsolete" in data["senses"][0]["raw_glosses"][0]:
        #lotta definitions start with "(obsolete) ..." so this just filters those words out
        pass
      else:
        lst.append({x: data[x] for x in releventKeys}) #add the word, pos, and lang_code from the JSON to a new dict in the list
        lst[-1]["definition"] = data["senses"][0]["raw_glosses"] #add definition key to current dict in list and add the def from JSON object
        lst[-1]["synonyms"] = []
        for sense in data["senses"]: #there's an array of senses and each can have synonyms, so loop and add any synonyms to the dict
          if "synonyms" in sense:
            for synonym in sense["synonyms"]:
              lst[-1]["synonyms"].append(synonym["word"])

def putWordEntriesTogether(list):
  ''' Each word is only associated with one pos, so there are multiple entries with the same word, but different pos and defs. 
      This function makes a new list of dicts with the following form:
      {word: word, defs:[[noun, def1], [verb, def2]], synonyms: [syn1, syn2]}'''
  newList = []
  for word in range(len(list)):
    if len(newList) == 0:
      newList.append({"word": lst[word]["word"], "definitions": [[lst[word]["pos"], lst[word]["definition"][0]]], "synonyms": lst[word]["synonyms"]})
    else:
      found = False
      for uniqueWord in range(len(newList)):
        if list[word]["word"] == newList[uniqueWord]["word"]:
          found = True
          newList[uniqueWord]["definitions"].append([list[word]["pos"], list[word]["definition"][0]])
          newList[uniqueWord]["synonyms"] += (list[word]["synonyms"])
          break
      if not found:
        newList.append({"word": lst[word]["word"], "definitions": [[lst[word]["pos"], lst[word]["definition"][0]]], "synonyms": lst[word]["synonyms"]})
  return newList

with open('english_words.json', 'w', encoding='utf-8') as f:
  json.dump(putWordEntriesTogether(lst), f)
