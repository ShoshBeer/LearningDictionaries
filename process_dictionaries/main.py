from utils.processWordDump import processWordDump
from utils.processWordFrequencies import processWordFrequencies
from utils.processRelatedWords import processRelatedWords
import json
import os

ExcludeTheseWords = [
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

def main(filename, wordsToExclude=ExcludeTheseWords, minWordLength=3, POStoInclude="noun verb adj", ExcludeProfanity=True):

  print('Creating draft dictionary')
  [draftDict, langCode] = processWordDump(filename, wordsToExclude, minWordLength, POStoInclude, ExcludeProfanity)

  if not os.path.exists(f'dictionaries/{langCode}'):
    os.makedirs(f'dictionaries/{langCode}')

  draft_file_path = f'dictionaries/{langCode}/{langCode}_draft_dict.json'
  with open(draft_file_path, 'w', encoding='utf-8') as f_draft:
    json.dump(draftDict, f_draft)

  print(f'Processing rough {langCode} dict')
  rough_file_path = f'dictionaries/{langCode}/{langCode}_rough_dict.json'
  processWordFrequencies(draft_file_path, rough_file_path, langCode)
  
  print(f'Smoothing related words in {langCode} game dictionary')
  smoothDict = processRelatedWords(rough_file_path, draft_file_path, langCode)

  smooth_file_path = f'dictionaries/{langCode}/{langCode}_smooth_dict.json'
  with open(smooth_file_path, 'w', encoding='utf-8') as f_smooth:
    json.dump(smoothDict, f_smooth)


main('process_dictionaries\kaikki.org-dictionary-Arabic.json', ExcludeProfanity=False)