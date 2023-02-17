
# To Do

---

## Revise Current Process

1. Download dictionary data from kaikki Wikitonary in target languages
2. Rewrite getData.py to be function that takes file name and language
   - Removes phrases with spaces
   - Filters nouns, verbs, and adjectives
     - Must examine the data in other langugages to see if json is also in that language
   - Creates list of dictionary objects with definition and synonyms
3. Next function in getData.py puts adjacent identical words into one dictionary object of the form: <br>`{word: word, defs:[[noun, def1], [verb, def2]], synonyms: [syn1, syn2]}`
4. At this point, the list of dictionary objects is written to a new file in JSON format
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
 - Add words from definitions to synonyms or new related words key'
  - Find data with words and their associated frequencies
    - Prefereably from source with multiple languages so can reuse funcitons
    - Thank you wordfreq!!
 - For each word above a certain frequency, add its frequency to the word list
 - Remove words below the frequency threshold