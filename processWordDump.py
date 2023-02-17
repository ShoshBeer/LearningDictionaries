import json
import wordfreq as wf

def makeLearningDict(filename, wordsToExclude, minWordLength = 3, POStoInclude = 'noun verb adj'):
  totalLines = sum(1 for line in open(filename, "r", encoding="utf-8")) # to print progress

  roughList = []
  with open(filename, "r", encoding="utf-8") as f:
    # I can also grab the language code from any word, might make things easier to do that than input language manually
    print(f'Reading {totalLines} total lines.')
    tenPercent = totalLines//10
    currentLine = 0

    for line in f:

      currentLine += 1
      if currentLine % tenPercent == 0:
        print(f'Reading {currentLine//tenPercent}0% complete')
      
      data = json.loads(line)

      if ' ' in data["word"] or len(data["word"]) < minWordLength or data["pos"] not in POStoInclude:
        # Skip multi-word phrases
        # By default, only take nouns, verbs, adjectives
        pass

      elif data["senses"][0].get("raw_glosses") == None:
        #idk what this takes out, the senses array has "raw_glosses" and "glosses" and they look like the same thing and seem like definitions
        #for some reason, some don't have "raw_glosses" so this just prevents an error when grabbing the definition
        #later I can look through the ones without it and check what's being skipped and if the definition is stored elsewhere
        pass

      elif any([x in data["senses"][0]["raw_glosses"][0].casefold() for x in wordsToExclude]):
        # Use this to filter out conjugations and other irrelevant words
        # Definitions in other languages are in English so might hardcode list (at least some of these types of words are also in other language defs)
        pass

      else:
        if len(roughList) == 0 or data["word"] != roughList[-1]["word"]:
          roughList.append({"word": data["word"], "definitions": [], "synonyms": []})
        for sense in range(len(data["senses"])): 
          #this could be skipped if the synonyms from educalingo are sufficient, but will keep for now
          roughList[-1]["definitions"].append([data["pos"], data["senses"][sense]["raw_glosses"][0]])
          if "synonyms" in data["senses"][sense]:
            for synonym in data["senses"][sense]["synonyms"]:
              roughList[-1]["synonyms"].append(synonym["word"])

  return roughList


if __name__ == "__main__":
  excluded = [
            "obsolete", "rare", "archaic", 
            "regional", "dialectal",
            "abbreviation", "initialism", "colloquial", "slang", 
            "simple past", "past participle", "simple present", "present participle", "future tense", "plural of", "plural future"
            "misspelling", "alternative form", "alternative spelling", "alternative letter", 
            "script ", "greek", "phonetic"
          ]
  testData = makeLearningDict('en', "kaikki.org-dictionary-English-words.json", excluded)

  with open('test_new_function_more_defs.json', 'w', encoding='utf-8') as f:
    json.dump(testData, f)
