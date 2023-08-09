import json
import os
from alive_progress import alive_bar
from filterAction import wordNotInList, wordInString

def processWordDump(filename, wordsToExclude, minWordLength = 3, POStoInclude = 'noun verb adj', ExcludeProfanity=True):

  # To print progress
  totalLines = sum(1 for line in open(filename, "r", encoding="utf-8"))

  draftDict = {}
  relationships = ["synonyms", "holonyms", "hypernyms", "hyponyms", "meronyms", "antonyms", "troponyms", "related"]
  badWord = None

  # Kaikki files have one JSON object per line
  # The file as a whole is NOT valid JSON
  with open(filename, "r", encoding="utf-8") as f:
    langCode = json.loads(f.readline())["lang_code"]

    with alive_bar(totalLines-1, title='Filtering words', stats=False) as bar:
      for line in f:

        # This line throws an error if the document is formatted!
        kaikkiEntry = json.loads(line)

        # For easier reading
        kaikkiWord = kaikkiEntry["word"]
        senses = kaikkiEntry["senses"]

        if badWord == kaikkiWord:
          continue

        if ' ' in kaikkiWord or len(kaikkiWord) < minWordLength or kaikkiEntry["pos"] not in POStoInclude:
          # Skip multi-word phrases
          # By default, only take nouns, verbs, adjectives
          continue

        else:
          clean = True

          if kaikkiWord == "יווני":
            print(draftDict)

          if kaikkiWord not in draftDict:
            print(f"adding {kaikkiWord} to draftdict")
            draftDict[kaikkiWord] = {"word": kaikkiWord, "definitions": [], "related words": []}
            draftEntry = draftDict[kaikkiWord]

          for sense in senses: 

            if ExcludeProfanity and "tags" in sense:
              print("exclude profanity block")
              for profanity in ["derogatory", "offensive", "vulgar"]:
                clean = wordNotInList(profanity, sense["tags"])
                if not clean:
                  badWord = kaikkiWord
                  break
              if not clean:
                break

            for gloss_type in ["raw_glosses", "glosses"]:
              if gloss_type in sense:
                print("Adding definition unless excluded word contained")
                print(sense[gloss_type][0])
                if not any([x in sense[gloss_type][0].casefold() for x in wordsToExclude]):
                  draftEntry["definitions"].append([kaikkiEntry["pos"], sense[gloss_type][0]])
                break
            else:
              break # Skip to next sense if this one has no definitions

            senseRelationships = (relationship for relationship in relationships if relationship in sense)

            for senseRelationship in senseRelationships:
              for count in range(len(sense[senseRelationship])):
                wordToAdd = wordNotInList(sense[senseRelationship][count]["word"], draftEntry["related words"], nested=True)
                if wordToAdd:
                  draftEntry["related words"].append([senseRelationship[:-1], wordToAdd])

          if len(draftEntry["definitions"]) == 0 or not clean:
            print(f"deleting this entry: {draftEntry['word']}")
            print(draftEntry["definitions"])
            print(clean)
            del draftEntry # Dirty words or words without definitions

        # KaikkiEntry could also have synonyms, antonyms, etc.
        if kaikkiWord in draftDict:
          wordRelationships = (relationship for relationship in relationships if relationship in kaikkiEntry)
          for wordRelationship in wordRelationships:
            for count in range(len(kaikkiEntry[wordRelationship])):
              wordToAdd = wordNotInList(kaikkiEntry[wordRelationship][count]["word"], draftEntry["related words"], nested=True)
              if wordToAdd:
                draftEntry["related words"].append([wordRelationship[:-1], wordToAdd])

        bar()

  return draftDict, langCode

if __name__ == "__main__":
  excluded = [
            "obsolete", "rare", "archaic", "dated"
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

  [draftDict, langCode] = processWordDump("process_dictionaries\kaikki.org-dictionary-Hebrew.json", excluded)

  if not os.path.exists(f'dictionaries/test/{langCode}'):
    os.makedirs(f'dictionaries/test/{langCode}')

  with open(f'dictionaries/test/{langCode}/{langCode}_draft_dict.json', 'w', encoding='utf-8') as f:
    json.dump(draftDict, f)
