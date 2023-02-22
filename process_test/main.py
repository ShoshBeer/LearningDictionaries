from utils.processWordDump import makeLearningDict
from utils.makeDictionaryByFrequency import makeGameDict
from utils.processRelatedWords import processRelatedWords
import json

def main(filename, wordsToExclude):

  print('Creating rough list')
  [roughList, langCode] = makeLearningDict(filename, wordsToExclude)

  rough_file = f'rough_list_{langCode}.json'
  with open(rough_file, 'w', encoding='utf-8') as f_rough:
    json.dump(roughList, f_rough)

  print(f'Processing rough {langCode} list')
  fineDict = makeGameDict(rough_file, langCode)

  fine_file = f'fine_dict_{langCode}.json'
  with open(fine_file, 'w', encoding='utf-8') as f_fine:
    json.dump(fineDict, f_fine)
  
  print(f'Smoothing related words in {langCode} game dictionary')
  smoothDict = processRelatedWords(fine_file, langCode)

  smooth_file = f'smooth_dict_{langCode}.json'
  with open(smooth_file, 'w', encoding='utf-8') as f_smooth:
    json.dump(smoothDict, f_smooth)

main('process_test\kaikki.org-dictionary-Hebrew.json', [])