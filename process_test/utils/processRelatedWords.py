import json
import wordfreq as wf

def processRelatedWords(filename, languageCode):
  proccessedWords = {}
  wordCount = 0

  def filterBadRW(type_word):
    if ' ' in type_word[1]:
      return False
    type_word.append(wf.word_frequency(type_word[1], languageCode))
    if type_word[2] < 0.00001:
      return False
    return True

  with open(filename, "r", encoding="utf-8") as f:
    wordsToProccess = json.load(f)
    for word in wordsToProccess:
      wordCount += 1
      proccessedWords[word] = wordsToProccess[word]
      proccessedWords[word]["related words"] = list(filter(filterBadRW, proccessedWords[word]["related words"]))

      if len(proccessedWords[word]["related words"]) < 5:
        wordCount -= 1
        del proccessedWords[word]
    
  return proccessedWords

if __name__ == "__main__":
  proccessedWords = processRelatedWords('test_freq_function_no_RW_filter.json', 'en')

  with open('test_freq_function_RW_filtered.json', 'w', encoding='utf-8') as f:
    json.dump(proccessedWords, f)
