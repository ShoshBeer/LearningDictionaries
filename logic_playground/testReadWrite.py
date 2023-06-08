import wordfreq as wf
from PyMultiDictionary import MultiDictionary, DICT_EDUCALINGO
from PyMultiDictionary._dictionary import InvalidLangCode
import json

'''
Given the file with the dictionary created by makeLearningDict(), this component will use the wordfreq module to make a more suitable word database for the Talking Circles game.
Method:
1. Use top_n_list for specified language to return the top 10 000 words in that langugae
2. For each of those top words, look for it in the dictionary
  -if it doesn't exist, next word (filters out other POS and unsuitable words filtered out by processWordDump.py)
  -add the frequency to the word data
  -put entry in new dictionary
3. Write list of words within frequency range to new file
'''

def makeGameDict(read_file, write_file, languageCode):
  dictionary = MultiDictionary()
  frequencyDict = wf.get_frequency_dict(languageCode)
  commonWords = wf.top_n_list(languageCode, 10000)
  eduSupportedLangs = ['bn', 'de', 'en', 'es', 'fr', 'hi', 'it', 'ja', 'jv', 'ko', 'mr', 'ms', 'pl', 'pt', 'ro', 'ru', 'ta', 'tr', 'uk', 'zh'] 
  #jv and mr are not supported by wordfreq (Javanese and Marathi)
  words = {}
  eduWords = True if languageCode in eduSupportedLangs else False

  def filterBadRW(type_word):
    keeping = True
    if ' ' in type_word[1]:
      keeping = False
    elif wf.word_frequency(type_word[1], languageCode) < 0.00001:
      keeping = False
    return keeping
  
  with open(read_file, "r", encoding="utf-8") as f_in, open(write_file, 'r+', encoding='utf-8') as f_out:
    f_out.write("{}")
    print('printing file', str(f_out.read()))
    output = json.load(f_out)
    for lexicon in f_in: 
      unfilteredWordList = json.loads(lexicon)
      wordCount = 0
      # noRW = 0
      # fewRW = 0
      # manyRW = 0

      for commonWord in commonWords:

        wordCount += 1
        if (wordCount % 100 == 0):
          print(f'{wordCount // 100}% processed')

        for word in unfilteredWordList:
          if commonWord == word["word"]:
            words[commonWord] = word
            words[commonWord]["frequency"] = frequencyDict[commonWord]

            if eduWords:
              EduSynonyms = dictionary.synonym(languageCode, commonWord, dictionary=DICT_EDUCALINGO)

              if len(EduSynonyms) > 0:
                for synonym in EduSynonyms:
                  words[commonWord]["related words"].append(["synonym", synonym])

            # words[commonWord]["related words"] = list(filter(filterBadRW, words[commonWord]["related words"]))

            output.update({commonWord: words[commonWord]})

            # if len(words[commonWord]["related words"]) == 0:
            #   noRW += 1
            # elif len(words[commonWord]["related words"]) < 5:
            #   fewRW += 1
            # else:
            #   manyRW += 1
            break
      
  return words

if __name__ == "__main__":
  words = makeGameDict("test_new_function_more_defs.json", "test_write.json", 'en')


  # [words, noRW, fewRW, manyRW] = makeGameDict("test_new_function_more_defs.json", 'en')

  # print(f'No RW: {noRW}, 1-4 RW: {fewRW}, 5+ RW: {manyRW}.')

  # with open('test_freq_function_no_RW_filter.json', 'w', encoding='utf-8') as f:
  #   json.dump(words, f)