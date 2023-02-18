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

          for relationship in ["synonyms", "hypermyns", "hyponyms", "meronyms", "antonyms", "related"]:
            if relationship in data["senses"][sense]:
              for relatedWord in data["senses"][sense][relationship]:
                if relatedWord["word"] not in roughList[-1]["word"] and roughList[-1]["word"] not in relatedWord["word"] and not any(relatedWord["word"] in similarWords for similarWords in roughList[-1]["related words"]):
                  roughList[-1]["related words"].append([relationship[:-1], relatedWord["word"]])

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
