import wordfreq as wf
import json

'''
Given the dictionary in the file english_words_from_full_list.json, this component will use the wordfreq module to make a more suitable word database for the Talking Circles game.
Method:
1. Use top_n_list for specified language to return the top 10 000 words in that langugae
2. For each of those top words, look for it in the dictionary
  -if it doesn't exist, next word (filters out other POS and unsuitable words filtered out by processWordDump.py)
  -add the frequency to the word data
  -put entry in new dictionary
3. Write list of words within frequency range to new file
'''

def makeGameDict(filename, languageCode):
  frequencyDict = wf.get_frequency_dict(languageCode)
  topWords = wf.top_n_list(languageCode, 10000)
  words = {}

  def filterBadRW(type_word):
    keeping = True
    if ' ' in type_word[1]:
      keeping = False
    elif wf.word_frequency(type_word[1], languageCode) < 0.000001:
      keeping = False
    return keeping
  
  with open(filename, "r", encoding="utf-8") as f:
    for dictionary in f: 
      data = json.loads(dictionary)
      wordCount = 0
      noRW = 0
      fewRW = 0
      manyRW = 0

      for commonWord in topWords:

        wordCount += 1
        if (wordCount % 100 == 0):
          print(f'{wordCount // 100}% processed')

        for word in data:
          if commonWord == word["word"]:
            words[commonWord] = word
            words[commonWord]["frequency"] = frequencyDict[commonWord]

            words[commonWord]["related words"] = list(filter(filterBadRW, words[commonWord]["related words"]))

            # for relatedWord in range(len(words[commonWord]["related words"])):
              # if ' ' in words[commonWord]["related words"][relatedWord][1]:
              #   words[commonWord]["related words"].pop(relatedWord)
              # if wf.word_frequency(words[commonWord]["related words"][relatedWord][1], languageCode) < 0.000001:
              #   pass
            if len(words[commonWord]["related words"]) == 0:
              noRW += 1
            elif len(words[commonWord]["related words"]) < 5:
              fewRW += 1
            else:
              manyRW += 1
            break
      
  return words, noRW, fewRW, manyRW

if __name__ == "__main__":
  [words, noRW, fewRW, manyRW] = makeGameDict("test_new_function_more_defs.json", 'en')

  print(f'No RW: {noRW}, 1-4 RW: {fewRW}, 5+ RW: {manyRW}.')

  with open('test_freq_function.json', 'w', encoding='utf-8') as f:
    json.dump(words, f)