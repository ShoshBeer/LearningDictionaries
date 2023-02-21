import wordfreq as wf
from PyMultiDictionary import MultiDictionary, DICT_EDUCALINGO
from PyMultiDictionary._dictionary import InvalidLangCode, _CACHED_SOUPS

# print('especially', wf.word_frequency('especially', 'en'))
# print('those', wf.word_frequency('those', 'en'))
# print('under', wf.word_frequency('under', 'en'))
# print('including', wf.word_frequency('including', 'en'))
# print('whose', wf.word_frequency('whose', 'en'))
# print('having', wf.word_frequency('having', 'en'))
# print('certain', wf.word_frequency('certain', 'en'))
# print('relating', wf.word_frequency('relating', 'en'))
# print('specifically', wf.word_frequency('specifically', 'en'))
# print('usually', wf.word_frequency('usually', 'en'))

dictionary = MultiDictionary()
nice = dictionary.synonym('en', 'nice')
for syn in nice:
  print(syn, wf.word_frequency(syn, 'en'))


# exclusions = [
#           "obsolete", "rare", "archaic", 
#           "regional", "dialectal",
#           "abbreviation", "initialism", "colloquial", "slang", 
#           "simple past", "past participle", "simple present", "present participle", "future tense", "plural of",
#           "misspelling", "alternative form", "alternative spelling", "alternative letter", 
#           "script ", "greek", "phonetic"
#         ]


#filter out numbers and etc and eg