import json
# import string
import re
import wordfreq as wf
# 6524 total words in the version 2 wordlist and 3038 have synonyms. 1696 of those with synonyms have 1-4, and 1342 have 5 or more synonyms
propsConjuncts = ['those', 'under', 'including', 'whose', 'having', 'certain', 'relating', 'specifically', 'usually']
with open("english_words_frequencies__dict_v2.json", "r+", encoding="utf-8") as f:
  dictionary = json.load(f)
  onePercent = 6524//100
  counter = 0
  noSyns = 0
  fewSyns = 0
  manySyns = 0
  for entry in dictionary:
    counter +=1
    if counter%onePercent == 0:
      print(f'{counter//onePercent}% processed')
    dictionary[entry]["related words"] = []
    for synonym in dictionary[entry]["synonyms"]:
      #check if each synonym is in the dictionary to remove really obscure words
      # if synonym in dictionary:
      #   dictionary[entry]["related words"].append(synonym)
      if synonym not in entry and entry not in synonym and synonym not in dictionary[entry]["related words"] and wf.word_frequency(synonym, 'en') > 0.0000001:
        dictionary[entry]["related words"].append(synonym)
    for definition in dictionary[entry]["definitions"]:
      for word in wf.tokenize(re.sub(r'\([^)]*\)', '', definition[1]), 'en'):
        if word not in entry and entry not in word and word not in dictionary[entry]["related words"] and word not in propsConjuncts and 0.00126 > wf.word_frequency(word, 'en') > 0.0000001:
          dictionary[entry]["related words"].append(word)
        # bareWord = word.translate(str.maketrans("","", string.punctuation)).casefold()
        # if bareWord not in entry and entry not in bareWord and bareWord not in dictionary[entry]["related words"] and len(bareWord) > 4 and bareWord in dictionary:
          # instead of checking if it's in the dictionary: check for a frequency threshold with freq_words and filter out prepositions and pronouns
          # if dictionary[bareWord]["definitions"][0][0] == "noun":
            # dictionary[entry]["related words"].append(bareWord)
    if len(dictionary[entry]["related words"]) > 4:
      manySyns += 1
    elif len(dictionary[entry]["related words"]) < 5:
      fewSyns += 1
    else:
      noSyns += 1


print(f"Words with no related words: {noSyns}")
print(f"Words with 4 or fewer related words: {fewSyns}")
print(f"Words with 5 or more related words: {manySyns}")

with open("english_words_freq_relwords_v2.json", "w", encoding="utf-8") as f:
  json.dump(dictionary, f)