import json
import wordfreq as wf

def processRelatedWords(filename, bigFilename, languageCode):
  proccessedWords = {}
  wordCountBefore = 0
  wordCountAfter = 0

  def filterBadRW(type_word):
    if ' ' in type_word[1]:
      return False
    type_word.append(wf.word_frequency(type_word[1], languageCode))
    if type_word[2] < 0.000001:
      # For de, removing RW with freqeuncy threshold > 1/100000 results in too few words, but a few hundred more with 1/1000000 threshold
      return False
    return True
  
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
      if wordCountBefore % (len(wordsToProccess) // 100) == 0:
        print(f'Initial filter: {wordCountBefore // (len(wordsToProccess) // 100)}%')
      proccessedWords[word] = wordsToProccess[word]
      proccessedWords[word]["related words"] = list(filter(filterBadRW, proccessedWords[word]["related words"]))

      if len(proccessedWords[word]["related words"]) < 5:
        del proccessedWords[word]

    for word in list(proccessedWords):
      # This goes through related words to make sure definitions are available
      wordCountAfter += 1
      if wordCountAfter % (len(proccessedWords) // 100) == 0:
        print(f'Definition processing: {wordCountAfter // (len(proccessedWords) // 100)}%')

      # proccessedWords[word]["related words"] = list(set(proccessedWords[word]["related words"])) # To remove duplicates

      # Related words will have words in the current dict first
      proccessedWords[word]["related words"].sort(key=inCurrentDict, reverse=True)

      i = 0
      while i < 5:
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

  return proccessedWords

if __name__ == "__main__":
  proccessedWords = processRelatedWords('es_rough_dict.json', 'es_draft_dict.json', 'es')

  with open('es_smooth_dict.json', 'w', encoding='utf-8') as f:
    json.dump(proccessedWords, f)
