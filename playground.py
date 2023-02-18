import wordfreq as wf

words = [['synonym', 'piece'], ['synonym', 'portion'], ['synonym', 'component'], ['synonym', 'element'], ['hyponym', 'fraction [⇒ thesaurus]'], ['hyponym', 'constituent'], ['hyponym', 'piece [⇒ thesaurus]'], ['hyponym', 'section'], ['hyponym', 'division'], ['hyponym', 'ingredient'], ['synonym', 'faction'], ['synonym', 'position'], ['synonym', 'role'], ['synonym', 'shed'], ['synonym', 'shoad'], ['synonym', 'shode'], ['synonym', 'chelek']]

dict = {"word": {"word": "wub", "related words": words}, 
"butt": {"word": "butt", "related words": [["synonym", "ass"], ["relate", "hole"]]}}

def noSpaces(partWord):
  return False if ' ' in partWord[1] else True

filteredWords = list(filter(noSpaces, words))

dict["word"]["related words"] = filteredWords
print(dict)

# for relatedWord in range(len(words)):
#   # print(words[commonWord]["related words"][relatedWord][1])
#   print(relatedWord, words[relatedWord][1])
#   if ' ' in words[relatedWord][1]:
#     words.pop(relatedWord)

# print(words)

# testrelated = [["synonym", "love"], ["synonym", "like"], ["hypernym", "feeling"]]
# testWord = "feel"

# if any(testWord in relatedEntry for relatedEntry in testrelated):
#   print('yes, this works')

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

# exclusions = [
#           "obsolete", "rare", "archaic", 
#           "regional", "dialectal",
#           "abbreviation", "initialism", "colloquial", "slang", 
#           "simple past", "past participle", "simple present", "present participle", "future tense", "plural of",
#           "misspelling", "alternative form", "alternative spelling", "alternative letter", 
#           "script ", "greek", "phonetic"
#         ]

# exampleDef = "The name of the Latin-script letter U."
# moreExample = "(obsolete) At the same time; simultaneously."

# print(moreExample.casefold())
# if any([x in moreExample.casefold() for x in exclusions]):
#   print("casefold: found exclusion")

# print(wf.tokenize(moreExample, 'en'))
# if any([x in wf.tokenize(moreExample, 'en') for x in exclusions]):
#   print("tokenize: found exclusion")

#filter out numbers and etc and eg