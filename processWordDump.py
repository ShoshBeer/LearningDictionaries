import json
import wordfreq as wf

def makeLearningDict(filename, wordsToExclude, minWordLength = 3, POStoInclude = 'noun verb adj'):
  totalLines = sum(1 for line in open(filename, "r", encoding="utf-8")) # to print progress

  roughList = []
  with open(filename, "r", encoding="utf-8") as f:
    # Can grab the language code from any word and return it to use in the frequency processing rather than manual input
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
        continue

      else:
        if len(roughList) == 0 or data["word"] != roughList[-1]["word"]:
          roughList.append({"word": data["word"], "definitions": [], "related words": []})

        for sense in range(len(data["senses"])): 
          if "raw_glosses" in data["senses"][sense]:
            if not any([x in data["senses"][sense]["raw_glosses"][0].casefold() for x in wordsToExclude]):
              roughList[-1]["definitions"].append([data["pos"], data["senses"][sense]["raw_glosses"][0]])

          elif "glosses" in data["senses"][sense]:
            if not any([x in data["senses"][sense]["glosses"][0].casefold() for x in wordsToExclude]):
              roughList[-1]["definitions"].append([data["pos"], data["senses"][sense]["glosses"][0]])

          if "synonyms" in data["senses"][sense]:
            for synonym in data["senses"][sense]["synonyms"]:
              if synonym["word"] not in roughList[-1]["word"] and roughList[-1]["word"] not in synonym["word"] and not any(synonym["word"] in similarWords for similarWords in roughList[-1]["related words"]):
                roughList[-1]["related words"].append(["synonym", synonym["word"]])
          
          if "hypermyns" in data["senses"][sense]:
            for hypernym in data["senses"][sense]["hypermyns"]:
              if hypernym["word"] not in roughList[-1]["word"] and roughList[-1]["word"] not in hypernym["word"] and not any(hypernym["word"] in similarWords for similarWords in roughList[-1]["related words"]):
                roughList[-1]["related words"].append(["hypernym", hypernym["word"]])

          if "hyponyms" in data["senses"][sense]:
            for hyponym in data["senses"][sense]["hyponyms"]:
              if hyponym["word"] not in roughList[-1]["word"] and roughList[-1]["word"] not in hyponym["word"] and not any(hyponym["word"] in similarWords for similarWords in roughList[-1]["related words"]):
                roughList[-1]["related words"].append(["hyponym", hyponym["word"]])

          if "meronyms" in data["senses"][sense]:
            for meronym in data["senses"][sense]["meronyms"]:
              if meronym["word"] not in roughList[-1]["word"] and roughList[-1]["word"] not in meronym["word"] and not any(meronym["word"] in similarWords for similarWords in roughList[-1]["related words"]):
                roughList[-1]["related words"].append(["meronym", meronym["word"]])

          if "antonyms" in data["senses"][sense]:
            for antonym in data["senses"][sense]["antonyms"]:
              if antonym["word"] not in roughList[-1]["word"] and roughList[-1]["word"] not in antonym["word"] and not any(antonym["word"] in similarWords for similarWords in roughList[-1]["related words"]):
                roughList[-1]["related words"].append(["antonym", antonym["word"]])

          if "related" in data["senses"][sense]:
            for related in data["senses"][sense]["related"]:
              if related["word"] not in roughList[-1]["word"] and roughList[-1]["word"] not in related["word"] and not any(related["word"] in similarWords for similarWords in roughList[-1]["related words"]):
                roughList[-1]["related words"].append(["related", related["word"]])

        if len(roughList[-1]["definitions"]) == 0:
          # These are some really weird and obscure words, so just going to filter these out (words without any glosses or raw_glosses in any sense for any POS)
          roughList.pop(-1)

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

  roughList = makeLearningDict("kaikki.org-dictionary-English-words.json", excluded)

  with open('test_new_function_more_defs.json', 'w', encoding='utf-8') as f:
    json.dump(roughList, f)
