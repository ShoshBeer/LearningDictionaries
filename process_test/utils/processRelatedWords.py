import json
import wordfreq as wf

def processRelatedWords(filename, bigFilename, languageCode):
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
    if type_word[2] < 0.00001:
      # For de, removing RW with freqeuncy threshold > 1/100000 results in too few words, but a few hundred more with 1/1000000 threshold
      return False
    return True

  with open(filename, "r", encoding="utf-8") as f:
    wordsToProccess = json.load(f)
    for word in wordsToProccess:
      wordCountBefore += 1
      if wordCountBefore % (len(wordsToProccess) // 100) == 0:
        print(f'Initial filter: {wordCountBefore // (len(wordsToProccess) // 100)}%')
      wordCountAfterFreqFilter += 1
      proccessedWords[word] = wordsToProccess[word]
      proccessedWords[word]["related words"] = list(filter(filterBadRW, proccessedWords[word]["related words"]))

      if len(proccessedWords[word]["related words"]) < 5:
        wordCountAfterFreqFilter -= 1
        del proccessedWords[word]

    for word in list(proccessedWords):
      # This goes through related words to make sure definitions are available
      wordCountAfterDefFilter += 1
      if wordCountAfterDefFilter % (len(proccessedWords) // 100) == 0:
        print(f'Definition processing: {wordCountAfterDefFilter // (len(proccessedWords) // 100)}%')

      countRW = 0
      for related in proccessedWords[word]["related words"]:
        if countRW > 5:
          break

        if related[1] in proccessedWords: #definite in specific should have hit here
          # If word is already in this dict, then I will grab it as the game runs
          print(f'{related[1]} for {word} is already in this dictionary')
          countRW += 1
          continue

        with open(bigFilename, "r", encoding="utf-8") as big_file:
          fullDictionary = json.load(big_file)
          if related[1] in fullDictionary: #agriculture should have hit here
            # If word is only in the unfiltered dict, add the definition to this one so it's easy to get in game
            related.append(fullDictionary[related[1]]["definitions"])
            print('Added def for RW: ', related[1], ' for word: ', word)
            countRW += 1
            continue

        # Otherwise, remove the word
        wordsWithoutDefs.append([word, related[1]])
        proccessedWords[word]["related words"].remove(related)
        print(f'Deleted RW {related[1]} for word {word}')
      
      if len(proccessedWords[word]["related words"]) < 5:
        # Doing this again to make sure that all words have at least 5 related words with definitions
        wordCountAfterDefFilter -= 1
        del proccessedWords[word]

  return proccessedWords, wordCountBefore, wordCountAfterFreqFilter, wordCountAfterDefFilter, wordsWithoutDefs

if __name__ == "__main__":
  [proccessedWords, wordCountBefore, wordCountAfterFreqFilter, wordCountAfterDefFilter, wordsWithoutDefs] = processRelatedWords('en_rough_dict.json', 'en_draft_dict.json', 'en')

  with open('en_RW_scraps.json', 'w', encoding='utf-8') as scraps:
    json.dump(wordsWithoutDefs, scraps)
  
    print(wordsWithoutDefs[0:10], len(wordsWithoutDefs))

  with open('en_RW_defs_test_2.json', 'w', encoding='utf-8') as f:
    json.dump(proccessedWords, f)
