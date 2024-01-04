import json
import os

from alive_progress import alive_bar

# from helpers.filterAction import wordNotInList, findRelationships # to run from here
from utils.helpers.filterAction import wordNotInList, findRelationships # to run from main.py

def processWordDump(filename, wordsToExclude, minWordLength = 3, POStoInclude = 'noun verb adj', ExcludeProfanity=True):

  totalLines = sum(1 for line in open(filename, "r", encoding="utf-8"))

  draftDict = {}
  badWord = None
  prevWord = None
  clean = True

  # Kaikki files have one JSON object per line, the file as a whole is NOT valid JSON
  with open(filename, "r", encoding="utf-8") as f:
    langCode = json.loads(f.readline())["lang_code"]

    with alive_bar(totalLines-1, title='Filtering words', stats=False) as bar:
      for line in f:

        # This line throws an error if the document is formatted!
        kaikkiEntry = json.loads(line)

        # For easier reading
        currentWord = kaikkiEntry["word"]
        senses = kaikkiEntry["senses"]

        if ' ' in currentWord or '-' in currentWord or len(currentWord) < minWordLength or kaikkiEntry["pos"] not in POStoInclude or badWord == currentWord:
          bar()
          continue

        if not prevWord or prevWord != currentWord: # When the word changes, check delete conditions for last added word
          if prevWord and len(draftEntry["definitions"]) == 0 or not clean:
            del draftDict[prevWord]
          
          draftDict[currentWord] = {"word": currentWord, "definitions": [], "related words": []} # add current word to draftDict
          draftEntry = draftDict[currentWord]
          prevWord = currentWord

        for relationship in findRelationships(kaikkiEntry):
          for count in kaikkiEntry[relationship]:
            wordToAdd = wordNotInList(count["word"], draftEntry["related words"], currentWord, True, ['-', ' '])
            if wordToAdd:
              draftEntry["related words"].append([relationship[:-1], wordToAdd])

        clean = True

        for sense in senses: 

          if ExcludeProfanity and "tags" in sense:
            for profanity in ["derogatory", "offensive", "vulgar"]:
              clean = wordNotInList(profanity, sense["tags"])
              if not clean:
                badWord = currentWord
                break
            if not clean:
              break

          for gloss_type in ["glosses", "raw_glosses"]:
            if gloss_type in sense:
              if not any([x in sense[gloss_type][0].casefold() for x in wordsToExclude]):
                draftEntry["definitions"].append([kaikkiEntry["pos"], sense[gloss_type][0]])
              break
          else:
            continue # Skip to next sense if this one has no definitions

          for relationship in findRelationships(sense):
            for count in sense[relationship]:
              wordToAdd = wordNotInList(count["word"], draftEntry["related words"], targetWord=currentWord, nested=True, excludedChars=['-', ' '])
              if wordToAdd:
                draftEntry["related words"].append([relationship[:-1], wordToAdd])

        bar()

  return draftDict, langCode

if __name__ == "__main__":
  excluded = [
            "obsolete", "rare", "archaic", "dated",
            "regional", "dialectal",
            "abbreviation", "initialism", "colloquial", "slang", 
            "simple past", "past participle", 
            "simple present", "present participle", 
            "future tense", "imperative", "subjunctive", "preterite", "gerund of", 
            "first-person", "third-person", "second-person",
            "plural of", "plural future", "singular present",
            "genitive", "dative", "accusative", "nominative", "all-case",
            "feminine", "masculine", "neuter", "all-gender",
            "misspelling", "alternative form", "alternative spelling", "defective spelling", "spelling of", "alternative letter", 
            "script ", "greek", "phonetic"
          ]

  [draftDict, langCode] = processWordDump("process_dictionaries\kaikki.org-dictionary-German.json", excluded)

  if not os.path.exists(f'dictionaries/test/{langCode}'):
    os.makedirs(f'dictionaries/test/{langCode}')

  with open(f'dictionaries/test/{langCode}/{langCode}_draft_dict.json', 'w', encoding='utf-8') as f:
    json.dump(draftDict, f)
