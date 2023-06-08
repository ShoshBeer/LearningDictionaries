import json

def showWords(filename):
  with open(filename, "r", encoding="utf-8") as f:
    wordsToUse = {}
    wordsExcluded = {}
    data = json.load(f)
    for word in data:
      if len(data[word]["related words"]) > 4:
        wordsToUse[word] = data[word]
      else:
        wordsExcluded[word] = data[word]
        
  return wordsToUse, wordsExcluded


if __name__ == "__main__":
  [wordsToUse, wordsExcluded] = showWords('test_freq_function.json')

  with open('see_english_words.json', 'w', encoding='utf-8') as f:
    json.dump(wordsToUse, f)

  with open('see_english_excluded.json', 'w', encoding='utf-8') as f:
    json.dump(wordsExcluded, f)