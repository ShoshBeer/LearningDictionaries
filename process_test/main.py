from utils.processWordDump import processWordDump
from utils.processWordFrequencies import processWordFrequencies
from utils.processRelatedWords import processRelatedWords
import json

def main(filename, wordsToExclude):

  print('Creating draft dictionary')
  [draftDict, langCode] = processWordDump(filename, wordsToExclude)

  draft_file = f'{langCode}_draft_dict.json'
  with open(draft_file, 'w', encoding='utf-8') as f_draft:
    json.dump(draftDict, f_draft)

  print(f'Processing rough {langCode} dict')
  roughDict = processWordFrequencies(draft_file, langCode)

  rough_file = f'{langCode}_rough_dict.json'
  with open(rough_file, 'w', encoding='utf-8') as f_rough:
    json.dump(roughDict, f_rough)
  
  print(f'Smoothing related words in {langCode} game dictionary')
  smoothDict = processRelatedWords(rough_file, draft_file, langCode)

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

main('process_test\kaikki.org-dictionary-Spanish.json', wordsToExclude)
