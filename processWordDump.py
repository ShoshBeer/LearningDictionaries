import json
import wordfreq as wf

def makeLearningDict(language, filename, wordsToExclude, minWordLength = 3, POStoInclude = 'noun verb adj'):
  totalLines = sum(1 for line in open(filename, "r", encoding="utf-8")) # to print progress

  roughList = []
  with open(filename, "r", encoding="utf-8") as f:
    print(f'Reading {totalLines} total lines.')
    tenPercent = totalLines//10
    currentLine = 0
    for line in f:
      currentLine += 1
      if currentLine % tenPercent == 0:
        print(f'Reading {currentLine//tenPercent}0% complete')
      data = json.loads(line)
      if ' ' in data["word"]:
        #skip multi-word phrases
        pass
      elif len(data["word"]) < minWordLength:
        pass
      elif data["pos"] not in POStoInclude:
        # by default, only take nouns, verbs, adjectives
        pass
      elif data["senses"][0].get("raw_glosses") == None:
        #idk what this takes out, the senses array has "raw_glosses" and "glosses" and they look like the same thing and seem like definitions
        #for some reason, some don't have "raw_glosses" so this just prevents an error when grabbing the definition
        #later I can look through the ones without it and check what's being skipped and if the definition is stored elsewhere
        pass
      elif any([x in data["senses"][0]["raw_glosses"][0].casefold() for x in wordsToExclude]):
        # can use this to filter out conjugations and other irrelevant words
        # definitions in other languages are in English so this might be a universal exclusion list (will see if these types of words are also in other language defs)
        # English exclusion list is 
        '''[
          "obsolete", "rare", "archaic", 
          "regional", "dialectal",
          "abbreviation", "initialism", "colloquial", "slang", 
          "simple past", "past participle", "simple present", "present participle", "future tense", "plural of",
          "misspelling", "alternative form", "alternative spelling", "alternative letter", 
          "script ", "greek", "phonetic"
        ]'''
        pass
      else:
        if len(roughList) != 0 and data["word"] == roughList[-1]["word"]:
          # If list isn't empty and word is same as previous entry, then add definition and synonyms to previous entry
          roughList[-1]["definitions"].append([data["pos"], data["senses"][0]["raw_glosses"][0]])
        else:
          roughList.append({"word": data["word"], "definitions": [[data["pos"], data["senses"][0]["raw_glosses"][0]]], "synonyms": []})
          # I can also grab the language code from here, might make things easier to do that than input it manually
          # roughList[-1]["definition"] = data["senses"][0]["raw_glosses"] #add definition key to current dict in list and add the def from JSON object
          # roughList[-1]["synonyms"] = []
        for sense in data["senses"]: 
          #there's an array of senses and each can have synonyms, so loop and add any synonyms to the dict
          #this could be skipped if the synonyms from educalingo are sufficient, but will keep for now
          if "synonyms" in sense:
            for synonym in sense["synonyms"]:
              roughList[-1]["synonyms"].append(synonym["word"])
  
  return roughList

excluded = [
          "obsolete", "rare", "archaic", 
          "regional", "dialectal",
          "abbreviation", "initialism", "colloquial", "slang", 
          "simple past", "past participle", "simple present", "present participle", "future tense", "plural of",
          "misspelling", "alternative form", "alternative spelling", "alternative letter", 
          "script ", "greek", "phonetic"
        ]
testData = makeLearningDict('en', "kaikki.org-dictionary-English-words.json", excluded)

with open('test_new_function.json', 'w', encoding='utf-8') as f:
  json.dump(testData, f)



# def putWordEntriesTogether(listOfDictObjects):
#   ''' Each word is only associated with one pos, so there are multiple entries with the same word, but different pos and defs. 
#       This function makes a new list of dicts with the following form:
#       {word: word, defs:[[noun, def1], [verb, def2]], synonyms: [syn1, syn2]}'''
#   print(f'Sorting {len(listOfDictObjects)} words')
#   newList = []
#   for word in range(len(listOfDictObjects)):
#     if len(newList) == 0:
#       newList.append({"word": listOfDictObjects[word]["word"], "definitions": [[listOfDictObjects[word]["pos"], listOfDictObjects[word]["definition"][0]]], "synonyms": listOfDictObjects[word]["synonyms"]})
#     elif listOfDictObjects[word]["word"] == newList[-1]["word"]:
#       newList[-1]["definitions"].append([listOfDictObjects[word]["pos"], listOfDictObjects[word]["definition"][0]])
#       newList[-1]["synonyms"] += (listOfDictObjects[word]["synonyms"])
#     else:
#       newList.append({"word": listOfDictObjects[word]["word"], "definitions": [[listOfDictObjects[word]["pos"], listOfDictObjects[word]["definition"][0]]], "synonyms": listOfDictObjects[word]["synonyms"]})
#   return newList
