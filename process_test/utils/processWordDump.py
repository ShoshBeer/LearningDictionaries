import json
import wordfreq as wf

def makeLearningDict(filename, wordsToExclude, minWordLength = 3, POStoInclude = 'noun verb adj'):
  totalLines = sum(1 for line in open(filename, "r", encoding="utf-8")) # to print progress

  roughDict = {}
  with open(filename, "r", encoding="utf-8") as f:
    langCode = json.loads(f.readline())["lang_code"]
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
        if data["word"] not in roughDict:
          roughDict[data["word"]] = {"word": data["word"], "definitions": [], "related words": []}

        for sense in range(len(data["senses"])): 
          if "raw_glosses" in data["senses"][sense]:
            if not any([x in data["senses"][sense]["raw_glosses"][0].casefold() for x in wordsToExclude]):
              roughDict[data["word"]]["definitions"].append([data["pos"], data["senses"][sense]["raw_glosses"][0]])

          elif "glosses" in data["senses"][sense]:
            if not any([x in data["senses"][sense]["glosses"][0].casefold() for x in wordsToExclude]):
              roughDict[data["word"]]["definitions"].append([data["pos"], data["senses"][sense]["glosses"][0]])

          for relationship in ["synonyms", "hypermyns", "hyponyms", "meronyms", "antonyms", "related"]:
            if relationship in data["senses"][sense]:
              for relatedWord in data["senses"][sense][relationship]:
                if relatedWord["word"].casefold() not in roughDict[data["word"]]["word"] and \
                   roughDict[data["word"]]["word"] not in relatedWord["word"].casefold() and \
                   not any(relatedWord["word"].casefold() in similarWord[1].casefold() for similarWord in roughDict[data["word"]]["related words"]):
                      roughDict[data["word"]]["related words"].append([relationship[:-1], relatedWord["word"]])

        if len(roughDict[data["word"]]["definitions"]) == 0:
          # These are some really weird and obscure words, so just going to filter these out (words without any glosses or raw_glosses in any sense for any POS)
          del roughDict[data["word"]]

  return roughDict, langCode

if __name__ == "__main__":
  excluded = [
            "obsolete", "rare", "archaic", 
            "regional", "dialectal",
            "abbreviation", "initialism", "colloquial", "slang", 
            "simple past", "past participle", 
            "simple present", "present participle", 
            "future tense", "imperative", "first-person", "third-person",
            "plural of", "plural future", "singular present",
            "genitive", "dative", "accusative", "nominative", "all-case",
            "feminine", "masculine", "neuter", "all-gender",
            "misspelling", "alternative form", "alternative spelling", "defective spelling", "alternative letter", 
            "script ", "greek", "phonetic"
          ]

  [roughDict, langCode] = makeLearningDict("kaikki.org-dictionary-English-words.json", excluded)

  with open('en_draft_dict.json', 'w', encoding='utf-8') as f:
    json.dump(roughDict, f)
