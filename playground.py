import wordfreq as wf
import json

processedWords = {}
count = 0
countWFilter = 0
with open('de_rough_dict.json', "r", encoding="utf-8") as f:
  wordsToProccess = json.load(f)

  def filterBadRW(type_word):
    if ' ' in type_word[1]:
      return False
    type_word.append(wf.word_frequency(type_word[1], "de"))
    if type_word[2] < 0.000001:
      return False
    return True

  for word in wordsToProccess:
    count += 1
    # countWFilter += 1
    processedWords[word] = wordsToProccess[word]
    processedWords[word]["related words"] = list(filter(filterBadRW, processedWords[word]["related words"]))

    if len(processedWords[word]["related words"]) > 4:
      countWFilter += 1
      del processedWords[word]

  print(count, countWFilter)

  # for word in processedWords:
  #   countAfterDefs += 1
  #   for relatedWord in processedWords[word]["related words"]:
  #     if relatedWord[1] in processedWords:
  #       pass
  #     elif relatedWord[1] in wordsToProccess:
  #       # print(wordsToProccess[relatedWord[1]]["definitions"])
  #       relatedWord.append(wordsToProccess[relatedWord[1]]["definitions"])
  #     else:
  #       processedWords[word]["related words"].remove(relatedWord)
      
   
  #   if len(processedWords[word]["related words"]) < 5:
  #     countAfterDefs -= 1
  #     del processedWords[word]
    
    

# with open('test_RW_defs.json', 'w', encoding="utf-8") as def_f:
#   json.dump(processedWords, def_f)




      # for relatedWord in proccessedWords[word]["related words"]:
      #   if proccessedWords[relatedWord[1]]:
      #     pass
      #   elif bigDict[relatedWord[1]]:
      #     relatedWord.append(bigDict[relatedWord[1]]["definitions"])
      #   else:
      #     proccessedWords[word]["related words"].remove(relatedWord)
      

# def filterBadDefs(POS_def):
#   if any([x in POS_def[1].casefold() for x in wordsToExclude]):
#     return False
#   return True

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

# exclusions = [
#           "obsolete", "rare", "archaic", 
#           "regional", "dialectal",
#           "abbreviation", "initialism", "colloquial", "slang", 
#           "simple past", "past participle", "simple present", "present participle", "future tense", "plural of",
#           "misspelling", "alternative form", "alternative spelling", "alternative letter", 
#           "script ", "greek", "phonetic"
#         ]


#filter out numbers and etc and eg