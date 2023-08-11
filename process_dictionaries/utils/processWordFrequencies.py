'''
Given the file with the dictionary created by processWordDump(), this component will use the wordfreq module to make a more suitable word database for the Talking Circles game.
Method:
1. Use top_n_list for specified language to return the top 10 000 words in that langugae
2. For each of those top words, look for it in the dictionary
  - If it doesn't exist, next word (filters out other POS and unsuitable words filtered out by processWordDump.py)
  - If it is top words and in draft dictionary:
    - Check if it's in the new dictionary, and move on to next top word if so
    - Otherwise, put entry in new dictionary
      - Add the frequency to the word data
      - If language is supported by PyMultiDictionary/Educalingo, get synonyms and add them to the related words list
        - If urllib URLError, ask user whether to try again or move on to next top word without adding to dictionary
        - If keyboard interrupt, move on to next top word without adding to dictionary
3. Write list of words within frequency range to new file
'''

import urllib.error
import json
import os

import wordfreq as wf
from alive_progress import alive_bar
from PyMultiDictionary import MultiDictionary, DICT_EDUCALINGO

def processWordFrequencies(draftFile, roughFile, languageCode):
  dictionary = MultiDictionary()
  frequencyDict = wf.get_frequency_dict(languageCode)
  commonWords = wf.top_n_list(languageCode, 10000)
  eduSupportedLangs = ['bn', 'de', 'en', 'es', 'fr', 'hi', 'it', 'ja', 'jv', 'ko', 'mr', 'ms', 'pl', 'pt', 'ro', 'ru', 'ta', 'tr', 'uk', 'zh'] 
  #jv and mr are not supported by wordfreq (Javanese and Marathi)
  eduWords = True if languageCode in eduSupportedLangs else False

  r_file = open(roughFile, 'a+', encoding="utf-8")
  if os.stat(roughFile).st_size == 0:
    json.dump({}, r_file)
  r_file.close()

  r_file = open(roughFile, 'r', encoding="utf-8")
  words = json.load(r_file)
  r_file.close()

  with open(draftFile, "r", encoding="utf-8") as f:
    for lexicon in f: 
      unfilteredWordDict = json.loads(lexicon)

      with alive_bar(10000, title="Sorting by frequency", stats=False) as bar:
        for commonWord in commonWords:

          for unfilteredWord in unfilteredWordDict:
            if commonWord == unfilteredWord:
              if unfilteredWord in words:
                break # Go to next common word, this one is already in the out file

              while True:
                try:
                  words[commonWord] = unfilteredWordDict[unfilteredWord]
                  words[commonWord]["frequency"] = frequencyDict[commonWord]

                  if eduWords:
                    EduSynonyms = dictionary.synonym(languageCode, commonWord, dictionary=DICT_EDUCALINGO)

                    if len(EduSynonyms) > 0:
                      for synonym in EduSynonyms:
                        if synonym.casefold() not in words[commonWord]["word"] and \
                          words[commonWord]["word"] not in synonym.casefold() and \
                          not any(synonym.casefold() in similarWord[1].casefold() for similarWord in words[commonWord]["related words"]):
                          words[commonWord]["related words"].append(["synonym", synonym])
                        
                  break # Out of the while loop

                except urllib.error.URLError:
                  print(f'Failed to get synonyms for {commonWord}')
                  ans = input("(y/n) Keep trying? ")
                  if ans == 'n':
                    break # Out of the while loop

                except KeyboardInterrupt:
                  print(f'Got stuck getting synonyms for {commonWord}')
                  break

              break # Go to next common word, this one is found

          bar()

  r_file = open(roughFile, 'w+', encoding="utf-8")
  json.dump(words, r_file)
  r_file.close()


if __name__ == "__main__":
  processWordFrequencies("dictionaries/es/es_draft_dict.json", 'dictionaries/es/es_rough_dict_write_test', 'es')
