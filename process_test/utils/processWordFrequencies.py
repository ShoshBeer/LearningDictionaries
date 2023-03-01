import wordfreq as wf
from PyMultiDictionary import MultiDictionary, DICT_EDUCALINGO
import json

'''
Given the file with the dictionary created by processWordDump(), this component will use the wordfreq module to make a more suitable word database for the Talking Circles game.
Method:
1. Use top_n_list for specified language to return the top 10 000 words in that langugae
2. For each of those top words, look for it in the dictionary
  -if it doesn't exist, next word (filters out other POS and unsuitable words filtered out by processWordDump.py)
  -add the frequency to the word data
  -put entry in new dictionary
3. Write list of words within frequency range to new file
'''

def processWordFrequencies(filename, languageCode):
  dictionary = MultiDictionary()
  frequencyDict = wf.get_frequency_dict(languageCode)
  commonWords = wf.top_n_list(languageCode, 10000)
  eduSupportedLangs = ['bn', 'de', 'en', 'es', 'fr', 'hi', 'it', 'ja', 'jv', 'ko', 'mr', 'ms', 'pl', 'pt', 'ro', 'ru', 'ta', 'tr', 'uk', 'zh'] 
  #jv and mr are not supported by wordfreq (Javanese and Marathi)
  words = {}
  eduWords = True if languageCode in eduSupportedLangs else False

  with open(filename, "r", encoding="utf-8") as f:
    for lexicon in f: 
      unfilteredWordDict = json.loads(lexicon)
      wordCount = 0

      for commonWord in commonWords:

        wordCount += 1
        if (wordCount % 100 == 0):
          print(f'{wordCount // 100}% processed')

        for word in unfilteredWordDict:
          if commonWord == unfilteredWordDict[word]["word"]:
            words[commonWord] = unfilteredWordDict[word]
            words[commonWord]["frequency"] = frequencyDict[commonWord]

            if eduWords:
              EduSynonyms = dictionary.synonym(languageCode, commonWord, dictionary=DICT_EDUCALINGO)

              if len(EduSynonyms) > 0:
                for synonym in EduSynonyms:
                  if synonym.casefold() not in words[commonWord]["word"] and \
                    words[commonWord]["word"] not in synonym.casefold() and \
                    not any(synonym.casefold() in similarWord[1].casefold() for similarWord in words[commonWord]["related words"]):
                    words[commonWord]["related words"].append(["synonym", synonym])

            break
      
  return words

if __name__ == "__main__":
  words = processWordFrequencies("en_draft_dict.json", 'en')

  with open('en_rough_dict_2.json', 'w', encoding='utf-8') as f:
    json.dump(words, f)