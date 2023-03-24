import json
import wordfreq as wf
import re

def processRelatedWords(filename, bigFilename, languageCode):
  proccessedWords = {}
  wordCountBefore = 0
  wordCountAfter = 0

  # def filterBadRW(type_word):
  #   if ' ' in type_word[1]:
  #     return False
  #   type_word.append(wf.word_frequency(type_word[1], languageCode))
  #   if type_word[2] < 0.000001:
  #     # For de, removing RW with freqeuncy threshold > 1/100000 results in too few words, but a few hundred more with 1/1000000 threshold
  #     return False
  #   return True
  
  def inCurrentDict(type_word):
    if type_word[1] in proccessedWords:
      return True
    else:
      return False
    
  def inBigDict(type_word):
    with open(bigFilename, "r", encoding="utf-8") as big_file:
      fullDictionary = json.load(big_file)
      if type_word[1] in fullDictionary:
        return fullDictionary[type_word[1]]["definitions"]
      else:
        return False

  with open(filename, "r", encoding="utf-8") as f:
    wordsToProccess = json.load(f)
    for word in wordsToProccess:
      wordCountBefore += 1
      # if wordCountBefore % (len(wordsToProccess) // 100) == 0:
      #   print(f'Initial filter: {wordCountBefore // (len(wordsToProccess) // 100)}%')
      proccessedWords[word] = wordsToProccess[word]

      # Go through each related word and apply regex to remove stuff in brackets
      for i in range(len(proccessedWords[word]["related words"])):
        proccessedWords[word]["related words"][i][1] = re.match('[^()]*(?<! )', proccessedWords[word]["related words"][i][1]).group()
      
      # proccessedWords[word]["related words"] = list(filter(filterBadRW, proccessedWords[word]["related words"]))

      if len(proccessedWords[word]["related words"]) < 1:
        del proccessedWords[word]

    for word in list(proccessedWords):
      # This goes through related words to make sure definitions are available
      wordCountAfter += 1
      # if wordCountAfter % (len(proccessedWords) // 100) == 0:
      #   print(f'Definition processing: {wordCountAfter // (len(proccessedWords) // 100)}%')

      # proccessedWords[word]["related words"] = list(set(proccessedWords[word]["related words"])) # To remove duplicates

      # Related words will have words in the current dict first
      proccessedWords[word]["related words"].sort(key=inCurrentDict, reverse=True)

      i = 0
      while i < 1:
        if i >= len(proccessedWords[word]["related words"]):
          del proccessedWords[word]
          break

        if inCurrentDict(proccessedWords[word]["related words"][i]):
          i += 1
        elif defs := inBigDict(proccessedWords[word]["related words"][i]):
          proccessedWords[word]["related words"][i].append(defs)
          i += 1
        else:
           del proccessedWords[word]["related words"][i]

  return proccessedWords, wordCountBefore, wordCountAfter

if __name__ == "__main__":
  [proccessedWords, wordCountBefore, wordCountAfter] = processRelatedWords('ko_rough_dict.json', 'ko_draft_dict.json', 'ko')

  print(f'Word count before removing words with <1 related words: {wordCountBefore}. After: {wordCountAfter}.')

  with open('ko_smooth_dict.json', 'w', encoding='utf-8') as f:
    json.dump(proccessedWords, f)


'''
Korean synonyms aren't on Educalingo
From Kaikki:
4309 words
67 words with 5+ related words
94 words with 4+ related words
183 words with 3+ related words
391 words with 2+ related words
979 words with 1+ related words
'''
