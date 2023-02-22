
# To Do

---

## Revise Current Process

1. Download dictionary data from kaikki Wikitonary in target languages
2. Rewrite getData.py to be function that takes file name, exclusion words, mininum number of letters, and parts of speech to include
   - Removes phrases with spaces
   - Filters to specified parts of speech (default nouns, verbs, and adjectives) and words that meet minimum length (default 3)
   - Puts adjacent identical words into one dictionary object
   - Related words are filtered if they contain or are contained by the entry word and duplicates are not added to the related words list
   - Creates list of dictionary objects with definition and related words in the form: <br>`{word: word, definitions:[[noun, def1], [verb, def2]], related words: [[synonym, word1], [hypernym, word2], [antonym, word3]]}`
4. At this point, the list of dictionary objects is written to a new file in JSON format
   - Can search here for English definitions of related words
   - Maybe will change to dictionary format for faster word lookup
5. Rewrite frequencyDict.py to generic function that takes filename and language parameter
   - wordfreq.get_frequency_dict(language)
   - wordfreq.top_n_list(language, 10000)
   - For each of the most common words, look for that word in the JSON dictionary and if it's there, add the frequency rating to the entry and add the entry to the new dictionary object
   - Write new dictionary with frequencies to new file
6. Rewrite relatedWords.py as function with language parameter
   - Loop through dictionary with frequencies
   - All related words should be filtered to prevent overlap with target word and other related words, certain frequency ranges, certain POS, multi word phrases?
      - Option: pull synonyms from PyMultiDictionary Educalingo and add to related words list
      - Option: add synonyms to related word list
      - Option: add filtered definition words to related word list
7. Dictionary with related words should be filtered to words that have enough related words, and definitions should be added for each from earlier kaikki word list

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