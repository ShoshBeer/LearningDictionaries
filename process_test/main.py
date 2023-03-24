from utils.processWordDump import processWordDump
from utils.processWordFrequencies import processWordFrequencies
from utils.processRelatedWords import processRelatedWords
import json

def main(filename, wordsToExclude, minWordLength):

  print('Creating draft dictionary')
  [draftDict, langCode] = processWordDump(filename, wordsToExclude, minWordLength)

  draft_file = f'{langCode}_draft_dict.json'
  with open(draft_file, 'w', encoding='utf-8') as f_draft:
    json.dump(draftDict, f_draft)

  print(f'Processing rough {langCode} dict')
  rough_file = f'{langCode}_rough_dict.json'
  processWordFrequencies(draft_file, rough_file, langCode)
  
  print(f'Smoothing related words in {langCode} game dictionary')
  smoothDict = processRelatedWords(rough_file, draft_file, langCode)

  smooth_file = f'{langCode}_smooth_dict.json'
  with open(smooth_file, 'w', encoding='utf-8') as f_smooth:
    json.dump(smoothDict, f_smooth)

wordsToExclude = [
            "obsolete", "rare", "archaic", 
            "regional", "dialectal",
            "abbreviation", "initialism", "colloquial", "slang", 
            "inflection of", "simple past", "past participle", 
            "simple present", "present participle", 
            "future tense", "imperative", "first-person", "third-person",
            "plural of", "plural future", "singular present",
            "genitive", "dative", "accusative", "nominative", "all-case",
            "feminine", "masculine", "neuter", "all-gender",
            "misspelling", "alternative form", "alternative spelling", 
            "defective spelling", "alternative letter", 
            "script ", "greek", "phonetic"
          ]

main('process_test\kaikki.org-dictionary-Portuguese.json', wordsToExclude, 3)
