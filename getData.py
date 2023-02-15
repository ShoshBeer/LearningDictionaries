import json

# totalLines = sum(1 for line in open("kaikki.org-dictionary-English-words.json", "r", encoding="utf-8"))
  
lst = []
releventKeys = ["word", "pos", "lang_code"]
exclusions = [
  "obsolete", "rare", "archaic", 
  "regional", "dialectal",
  "abbreviation", "initialism", "colloquial", "slang", 
  "simple past", "simple present", "future tense", "plural of",
  "misspelling", "alternative form", "alternative spelling", "alternative letter", 
  "script ", "greek", "phonetic"
]
with open("kaikki.org-dictionary-English-words.json", "r", encoding="utf-8") as f:
  # there are 1,194,876 lines in this file
  print(f'Reading 1,194,876 lines')
  tenPercent = 1194876//10
  currentLine = 0
  for line in f: 
    currentLine += 1
    if currentLine % tenPercent == 0:
      print(f'Reading {currentLine//tenPercent}0% complete')
    data = json.loads(line)
    if ' ' in data["word"]:
      #skip multi-word phrases
      pass
    elif len(data["word"]) < 3:
      #no 1 or 2 letter words for English, may have to adjust for other languages
      pass
    elif data["pos"] not in "noun verb adj":
      #only take nouns, verbs, adjectives. May add in adverbs in later developments.
      pass
    elif data["senses"][0].get("raw_glosses") == None:
      #idk what this takes out, the senses array has "raw_glosses" and "glosses" and they look like the same thing and seem like definitions
      #for some reason, some don't have "raw_glosses" so this just prevents an error when grabbing the definition
      #later I can look through the ones without it and check what's being skipped and if the definition is stored elsewhere
      pass
    elif any([x in data["senses"][0]["raw_glosses"][0].casefold() for x in exclusions]) :
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
  print(f'Sorting {len(lst)} words')
  newList = []
  for word in range(len(list)):
    if len(newList) == 0:
      newList.append({"word": lst[word]["word"], "definitions": [[lst[word]["pos"], lst[word]["definition"][0]]], "synonyms": lst[word]["synonyms"]})
    elif list[word]["word"] == newList[-1]["word"]:
      newList[-1]["definitions"].append([list[word]["pos"], list[word]["definition"][0]])
      newList[-1]["synonyms"] += (list[word]["synonyms"])
    else:
      newList.append({"word": lst[word]["word"], "definitions": [[lst[word]["pos"], lst[word]["definition"][0]]], "synonyms": lst[word]["synonyms"]})
  return newList

with open('english_words_from_full_list_v2.json', 'w', encoding='utf-8') as f:
  json.dump(putWordEntriesTogether(lst), f)
