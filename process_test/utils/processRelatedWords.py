import json
import wordfreq as wf

def processRelatedWords(filename, languageCode):
  proccessedWords = {}
  wordCountBefore = 0
  wordCountAfterFreqFilter = 0
  wordCountAfterDefFilter = 0
  wordsWithoutDefsAfter = 0
  wordsWithoutDefs = []

  def filterBadRW(type_word):
    if ' ' in type_word[1]:
      return False
    type_word.append(wf.word_frequency(type_word[1], languageCode))
    if type_word[2] < 0.000001:
      # For de, removing RW with freqeuncy threshold > 1/100000 results in too few words, but a few hundred more with 1/1000000 threshold
      return False
    return True

  with open(filename, "r", encoding="utf-8") as f:
    wordsToProccess = json.load(f)
    for word in wordsToProccess:
      wordCountBefore += 1
      wordCountAfterFreqFilter += 1
      proccessedWords[word] = wordsToProccess[word]
      proccessedWords[word]["related words"] = list(filter(filterBadRW, proccessedWords[word]["related words"]))

      if len(proccessedWords[word]["related words"]) < 5:
        wordCountAfterFreqFilter -= 1
        del proccessedWords[word]

    for word in list(proccessedWords):
      # This goes through related words to make sure definitions are available
      wordCountAfterDefFilter += 1
      for related in proccessedWords[word]["related words"]:
        if related[1] in proccessedWords: #definite in specific should have hit here
          # If word is already in this dict, then I will grab it as the game runs
          # print(f'{related[1]} for {word} is already in this dictionary')
          pass
        elif related[1] in wordsToProccess: #agriculture should have hit here
          # If word is only in the unfiltered dict, add the definition to this one so it's easy to get in game
          related.append(wordsToProccess[related[1]]["definitions"])
          # print('Added def for RW: ', related[1], ' for word: ', word)
        else: #singular for word specific should have hit here and grapefruit for hybrid
          # Otherwise, remove the word
          wordsWithoutDefs.append([word, related[1]])
          # proccessedWords[word]["related words"].remove(related)
          # print(f'Deleted RW {related[1]} for word {word}')
      
      if len(proccessedWords[word]["related words"]) < 5:
        # Doing this again to make sure that all words have at least 5 related words with definitions
        wordCountAfterDefFilter -= 1
        del proccessedWords[word]

  return proccessedWords, wordCountBefore, wordCountAfterFreqFilter, wordCountAfterDefFilter, wordsWithoutDefs

if __name__ == "__main__":
  [proccessedWords, wordCountBefore, wordCountAfterFreqFilter, wordCountAfterDefFilter, wordsWithoutDefs] = processRelatedWords('test_freq_function_no_RW_filter.json', 'en')

  print(wordsWithoutDefs[0:20])

  with open('en_smooth_dict.json', 'w', encoding='utf-8') as f:
    json.dump(proccessedWords, f)
