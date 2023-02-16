'''
Here I will use wordfreq's top most common words, summon each word with the PyMultiDictionary, filter out certain parts of speech, and make a dictionary with the definitions, synonyms, and antonyms.
Will see how that dictionary compares to the one made with the Wikitonary dictionary that was filtered by POS and frequency afterward.
'''
import wordfreq as wf
from PyMultiDictionary import MultiDictionary, DICT_EDUCALINGO #only supports half the languages that wordfreq does :(

dictionary = MultiDictionary()
print(dictionary.meaning('en', 'suffice', dictionary=DICT_EDUCALINGO))

# def makeDict(language, max_length, file='freqDictTest.json'):
#   constructedDictionary = {} #can use random.choice(list(dictionary.values())) to get a random word from the dictionary
#   topWords = wf.top_n_list(language, max_length)
#   for commonWord in topWords:
