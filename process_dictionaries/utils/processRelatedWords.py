import json
from functools import partial

from alive_progress import alive_bar

# from helpers.relatedWordsHelpers import filterBadRW, inCurrentDict, inBigDict # to run from here
from utils.helpers.relatedWordsHelpers import filterBadRW, inCurrentDict, inBigDict # to run from main.py

def processRelatedWords(filename, bigFilename, languageCode):
  processedWords = {}

  with open(filename, "r", encoding="utf-8") as f:
    wordsToProcess = json.load(f)

    with alive_bar(len(wordsToProcess), title="Filtering related words", stats=False) as bar:
      for word in wordsToProcess:
        processedWords[word] = wordsToProcess[word]
        processedWords[word]["related words"] = list(filter(lambda RW: filterBadRW(RW, languageCode), processedWords[word]["related words"]))

        if len(processedWords[word]["related words"]) < 5:
          del processedWords[word]
        
        bar()

    with alive_bar(len(processedWords), title="Sorting related words", stats=False) as bar:
      for word in list(processedWords):
        # This goes through related words to make sure definitions are available

        # Related words will have words in the current dict first
        processedWords[word]["related words"].sort(key=partial(inCurrentDict, processed=processedWords), reverse=True)

        i = 0
        while i < 5:
          if i >= len(processedWords[word]["related words"]):
            del processedWords[word]
            break

          if inCurrentDict(processedWords[word]["related words"][i], processedWords):
            i += 1
          elif defs := inBigDict(processedWords[word]["related words"][i], bigFilename):
            processedWords[word]["related words"][i].append(defs)
            i += 1
          else:
            del processedWords[word]["related words"][i]

        bar()

  return processedWords

if __name__ == "__main__":
  processedWords = processRelatedWords('dictionaries/es/es_rough_dict.json', 'dictionaries/es/es_draft_dict.json', 'es')

  with open('dictionaries/es/es_smooth_dict.json', 'w', encoding='utf-8') as f:
    json.dump(processedWords, f)
