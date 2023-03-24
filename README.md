
# To Do

---

## Revise Current Process

1. Download dictionary data from kaikki Wikitonary in target languages
2. processWordDump.py has function: `processWordDump(filename, wordsToExclude, minWordLength, POStoInclude)`
    - Removes phrases with spaces
    - Filters to specified parts of speech (default nouns, verbs, and adjectives) and words that meet minimum length (default 3)
    - Filters out word senses with vulgar, derogatory, or offensive tag
    - Puts adjacent identical words into one dictionary object
    - Related words are filtered if they contain or are contained by the entry word and duplicates are not added to the related words list
    - Creates dictionary of words with dictionary object values with definition and related words in the form: <br>`"word": {word: "word", definitions:[[noun, def1], [verb, def2]], related words: [[synonym, word1], [hypernym, word2], [antonym, word3]]}`
    - Return new dictionary of words
3. processWordFrequencies.py has function: `processWordFrequencies(draftFile, roughFile, languageCode)`
    - If the roughFile is empty, create an empty dictionary in it
    - Read in the contents of roughFile (empty dictionary if this is the first attempt)
    - For each of the most common 10,000 words retrieved by `wordfreq`, look for that word in the draft dictionary and if it's there:
      - Check if it's already in the roughFile, then
      - Try:
        - Add the frequency rating to the entry and add the entry to the new dictionary object
        - If in Educalingo, add synonyms from Educalingo to related words in the new dictionary using `PyMultiDictionary` if not in target word and no duplicate -> **this can raise URLError**
      - Except:
        - User chooses whether to try again to get those synonyms and if it's skipped, then the word won't be added at all 
      - Option for more related words: add select words from definitions
    - Write updated dictionary to roughFile
4. processRelatedWords.py has function `processRelatedWords(filename)`
    - Related words with spaces and below a frequency threshold are filtered
      - May add frequency of each for sorting related words by relevance later
    - Dictionary is filtered to words with 5+ related words
    - Related word list for each word is sorted to have the words in the new dictionary first
    - Loop through each word and each related word
       - If it's in the new dictionary, move on and can get the definition when needed
       - Check the draft dictionary for the word, and add the definition to the related word array if found
       - If it's not in the draft dicitonary, remove the related word
    - Return new dictionary

## Current Data Enhancements

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
 - Add definitions to synonyms and related words