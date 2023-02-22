
# To Do

---

## Revise Current Process

1. Download dictionary data from kaikki Wikitonary in target languages
2. processWordDump.py has function: `makeLearningDict(filename, wordsToExclude, minWordLength, POStoInclude)`
    - Removes phrases with spaces
    - Filters to specified parts of speech (default nouns, verbs, and adjectives) and words that meet minimum length (default 3)
    - Puts adjacent identical words into one dictionary object
    - Related words are filtered if they contain or are contained by the entry word and duplicates are not added to the related words list
    - Creates list of dictionary objects with definition and related words in the form: <br>`{word: word, definitions:[[noun, def1], [verb, def2]], related words: [[synonym, word1], [hypernym, word2], [antonym, word3]]}`
    - Return new list of words
    - Makes sense to write to a new file for getting related words defs later
    - **May change to dictionary format for faster word lookup** (unecessary if synonyms are all always in processed list)
3. makeDictionaryByFrequency.py has function: `makeGameDict(filename, languageCode)`
    - For each of the most common words retrieved by `wordfreq`, look for that word in the JSON dictionary and if it's there:
      - Add the frequency rating to the entry and add the entry to the new dictionary object
      - Add synonyms from Educalingo to related words in the new dictionary using `PyMultiDictionary` if not in target word and no duplicate
      - Option for more related words: add select words from definitions
    - Return new dictionary
4. processRelatedWords.py has function `processRelatedWords(filename)`
    - Related words with spaces and below a frequency threshold are filtered
      - May add frequency of each for sorting related words by relevance later
    - Dictionary is filtered to words with 5+ related words
    - Definitions are retrieved for related words
    - Least common word in top 10000 for English is 5.89e-06 which is lower than the freqeuncy cutoff for synonyms, so every synonym definition should already be in the processed dict
    - Return new dictionary

## Current Data Enhancements

 - Add definitions to synonyms and related words
 - **Make files for other languages**

## Completed

---

 - Remove duplicate synonyms
 - Add words from definitions to synonyms or new related words key
  - Find data with words and their associated frequencies
    - Prefereably from source with multiple languages so can reuse funcitons
    - Thank you wordfreq!!
 - For each word above a certain frequency, add its frequency to the word list
 - Remove words below the frequency threshold