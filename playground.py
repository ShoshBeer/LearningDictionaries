import wordfreq as wf
import json
import random

# words = {"that": {"word": "that", "definitions": [["noun", "(philosophy) Something being indicated that is there; one of those."]], "related words": [["relate", "which"]], "frequency": 0.010232929922807542}}
# word1 = '"that": {"word": "that", "definitions": [["noun", "(philosophy) Something being indicated that is there; one of those."]], "related words": [["relate", "which"]], "frequency": 0.010232929922807542}'

# word2 = '"you": {"word": "you", "definitions": [["verb", "(transitive) To address (a person) using the pronoun you (in the past, especially to use you rather than thou, when you was considered more formal)."]], "related words": [], "frequency": 0.009549925860214359}'

wordsToAdd = [{"word": "this"}, {"word": "are"}, {"word": "abide"}, {"word": "arise"}, {"word": "attend"}]

def readJson():
  # Starting with a JSON object in the file
  file = open('test-write-json.json', 'r+', encoding="utf-8")
  if len(file.readline()) == 0:
    json.dump({}, file)
  file.close()
  
  # Now this is buffered content I can work with
  file = open('test-write-json.json', 'r', encoding="utf-8")
  data = json.load(file)
  file.close()

   # Now I work with the content
  for word in wordsToAdd:
    while True:
      failSometimes = random.random()
      try:
        if failSometimes < 0.2:
          raise KeyError
        
        if word["word"] in data:
          break

        print(f"Adding word: {word['word']}")
        data[word["word"]] = word
        break

      except KeyError:
        print(f'Failed to get synonyms for {word["word"]}')
        ans = input("(y/n) Keep trying? ")
        if ans == 'n':
          break

  # Now I write the stuff I just did to the file (I update the object with my new object)
  file = open('test-write-json.json', 'w+', encoding="utf-8")
  json.dump(data, file)
  file.close()

  return None

readJson()




  










# wordsToExclude = [
#             "obsolete", "rare", "archaic", 
#             "regional", "dialectal",
#             "abbreviation", "initialism", "colloquial", "slang", 
#             "simple past", "past participle", 
#             "simple present", "present participle", 
#             "future tense", "imperative", "first-person", "third-person",
#             "plural of", "plural future", "singular present",
#             "genitive", "dative", "accusative", "nominative", "all-case",
#             "feminine", "masculine", "neuter", "all-gender",
#             "misspelling", "alternative form", "alternative spelling", "defective spelling", "alternative letter", 
#             "script ", "greek", "phonetic"
#           ]
# langCode = 'de'
# with open('smooth_dict_de.json', "r", encoding="utf-8") as f:
#   extraSmoothDict = {}
#   wordsToProccess = json.load(f)
#   for word in wordsToProccess:
#     extraSmoothDict[word] = wordsToProccess[word]
#     extraSmoothDict[word]["definitions"] = list(filter(filterBadDefs, extraSmoothDict[word]["definitions"]))

#     if len(extraSmoothDict[word]["definitions"]) == 0:
#       del extraSmoothDict[word]



# test_freq_function_no_RW_filter.json: No RW: 954, 1-4 RW: 502, 5+ RW: 5161.

