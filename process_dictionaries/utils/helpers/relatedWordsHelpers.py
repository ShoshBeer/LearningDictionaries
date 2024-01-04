import json

import wordfreq as wf

def filterBadRW(type_word, languageCode):
  if ' ' in type_word[1]:
    return False
  type_word.append(wf.word_frequency(type_word[1], languageCode))
  if type_word[2] < 0.000001:
    # For de, removing RW with freqeuncy threshold > 1/100000 results in too few words, but a few hundred more with 1/1000000 threshold
    return False
  return True

def inCurrentDict(type_word, processed):
  if type_word[1] in processed:
    return True
  else:
    return False
  
def inBigDict(type_word, bigFileName):
  with open(bigFileName, "r", encoding="utf-8") as big_file:
    fullDictionary = json.load(big_file)
    if type_word[1] in fullDictionary:
      return fullDictionary[type_word[1]]["definitions"]
    else:
      return False