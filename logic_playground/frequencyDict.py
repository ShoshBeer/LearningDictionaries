import wordfreq as wf
import json

'''
Given the dictionary in the file english_words_from_full_list.json, this component will use the wordfreq module to make a more suitable word database for the Talking Circles game.
Method:
1. Use top_n_list for specified language to return the top 10 000 words in that langugae
2. For each of those top words, look for it in the dictionary
  -if it doesn't exist, next word (filters out other POS and maybe contractions)
  -add the frequency to the word data
  -put entry in new list
3. Write list of common word with frequencies to new file
4. More processing on new file done elsewhere (to improve related words and their defs)
'''

englishDict = wf.get_frequency_dict('en')
topWords = wf.top_n_list('en', 10000)
words = {}
with open("english_words_from_full_list_v2.json", "r", encoding="utf-8") as f:
  for dictionary in f: 
    data = json.loads(dictionary)
    wordCount = 0
    for commonWord in topWords:
      wordCount += 1
      if (wordCount % 100 == 0):
        print(f'{wordCount // 100}% processed')
      for word in data:
        if commonWord == word["word"]:
          word["frequency"] = englishDict[commonWord]
          words[commonWord] = word
          break

with open('english_words_frequencies__dict_v2.json', 'w', encoding='utf-8') as f:
  json.dump(words, f)


