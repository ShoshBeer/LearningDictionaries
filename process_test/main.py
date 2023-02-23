from utils.processWordDump import makeLearningDict
from utils.makeDictionaryByFrequency import makeGameDict
from utils.processRelatedWords import processRelatedWords
import json

def main(filename, wordsToExclude):

  print('Creating draft list')
  [draftList, langCode] = makeLearningDict(filename, wordsToExclude)

  draft_file = f'{langCode}_draft_list.json'
  with open(draft_file, 'w', encoding='utf-8') as f_draft:
    json.dump(draftList, f_draft)

  print(f'Processing draft {langCode} list')
  roughDict = makeGameDict(draft_file, langCode)

  rough_file = f'{langCode}_rough_dict.json'
  with open(rough_file, 'w', encoding='utf-8') as f_rough:
    json.dump(roughDict, f_rough)
  
  print(f'Smoothing related words in {langCode} game dictionary')
  smoothDict = processRelatedWords(rough_file, langCode)

  smooth_file = f'{langCode}_smooth_dict.json'
  with open(smooth_file, 'w', encoding='utf-8') as f_smooth:
    json.dump(smoothDict, f_smooth)

wordsToExclude = [
            "obsolete", "rare", "archaic", 
            "regional", "dialectal",
            "abbreviation", "initialism", "colloquial", "slang", 
            "simple past", "past participle", 
            "simple present", "present participle", 
            "future tense", "imperative", "first-person", "third-person",
            "plural of", "plural future", "singular present",
            "genitive", "dative", "accusative", "nominative", "all-case",
            "feminine", "masculine", "neuter", "all-gender",
            "misspelling", "alternative form", "alternative spelling", "defective spelling", "alternative letter", 
            "script ", "greek", "phonetic"
          ]

main('process_test\kaikki.org-dictionary-German.json', wordsToExclude)