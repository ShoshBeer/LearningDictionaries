
# Learning Dictionaries

## Table of Contents

1. [About](#about)
2. [Dictionary Format](#dictionary-format)
3. [How to Use](#how-to-use)
4. [Citations](#citations)
5. [How it Works](#how-it-works)
6. [Next Steps](#next-steps)

## About

This project provides a method of getting dictionaries in different languages suitable for language learning and language games. I created it after failing to find a suitable resource for my project [Talking in Circles](https://github.com/ShoshBeer/talking-circles). 

To create this project, I made use of a few wonderful resources: 
 - [kaikki.org](https://kaikki.org/index.html) provides dictionaries in many languages extracted from [Wikitionary](https://en.wiktionary.org/wiki/Wiktionary:Main_Page) and includes related words and other metadata
 - [wordfreq](https://github.com/rspeer/wordfreq) provides word frequency data for many languages and has a few super helpful functions for this project
 - [PyMultiDictionary](https://pypi.org/project/PyMultiDictionary/) provides extra synonyms in many languages by making use of [educalingo.com](https://educalingo.com/en/dic-en) 

The result of this method is a dictionary in a specified language with English definitions, frequencies, and related words of the most common words. The method can easily be adjusted to customize the frequency threshold, the parts of speech, and other parameters. 

Definitions with a vulgar, derogatory, and offensive tag are filtered out by default, but can be included. **Note: if a word has a clean definition then it will be included with its clean definition even if it has other inappropriate definitions.**

---

## Dictionary Format

Three JSON files are created in the process of making the dictionary, each with more processing than the last. An example entry in the final dictionary has the following format:

```
"enterprise": {
  "word": "enterprise", 
  "definitions": [
    [
      "noun", 
      "A company, business, organization, or other purposeful endeavor."
    ], 
    [
      "verb", 
      "(intransitive) To undertake an enterprise, or something hazardous or difficult."
    ],
    ...
  ], 
  "related words": [
    ["synonym", "business", 0.000363], 
    ["hyponym", "corporation", 3.89e-05], 
    ["meronym", "factory", 3.55e-05, [
      ["noun", "A building or other place where manufacturing takes place."],
      ["noun", "(programming) In a computer program or library, a function, method, etc. which creates an object."],
      ...
    ]],
    ...
  ],
  "freqeuncy": 2.39883291901949e-05
}
```

Since "factory" is not an entry in the final dictionary, an array of its definitions is appended to the related word array.

More information on the frequency data can be found on the [wordfreq GitHub repository](https://github.com/rspeer/wordfreq).

---

## How to Use

### Process a Dictionary From Scratch

1. Download the `process_dictionaries/` folder from this repo.
2. Install required modules and packages listed in requirements.txt with `pip install -r requirements.txt`.
2. Go to [Kaikki.org](https://kaikki.org/dictionary/) and download a dictionary for one of the [40 languages supported by wordfreq](https://github.com/rspeer/wordfreq#sources-and-supported-languages) to the `process_dictionaries/` folder.
3. Open `main.py` and change the parameters at the bottom of the file:
   - Write the file name of the Kaikki dictionary you want to proces
   - Optionally, add words to exclude, specify minimum word length and parts of speech, and include profanity. See [How it Works Part 1](#part-1-remove-extraneous-data-from-kaikki-dictionary) for more information on these parameters.
4. Run `main.py`
5. You now have three dictionaries with varying levels of processing applied.

### Download an Already Made Dictionary

*Note: The dictionaries I have processed are available for download in this repo, but they have not been recreated after each feature addition or bug fix. Therefore, the ready-made dictionaries may not fit the format exactly, may not have all the words expected, may have more words than expected, may have duplicates, and may have other issues.*

1. Find the language(s) you want in the `dictionaries/` folder, organized by language code.
2. Download the files you want.

---

## Citations

Many thanks to the authors of the freely-available data tools that allowed me to build this app!

Dictionary data for all languages comes from https://kaikki.org/dictionary/, which includes a list of words and phrases in that language, definitions in English for every sense, and related words for some words.

> Tatu Ylonen: Wiktextract: Wiktionary as Machine-Readable Structured Data, Proceedings of the 13th Conference on Language Resources and Evaluation (LREC), pp. 1317-1325, Marseille, 20-25 June 2022.

---

Word freqeuncy data for all languages comes from [wordfreq](https://zenodo.org/record/7199437), a very useful tool that I used to obtain the frequency score of a word and a list of the most common words in a specified language.

> Robyn Speer. (2022). rspeer/wordfreq: v3.0 (v3.0.2). Zenodo. https://doi.org/10.5281/zenodo.7199437

---

Extra synonyms for many languages are sourced from PyMultiDictionary. The languages available are listed on the project page, but some languages don't have many synonyms.

> Pablo R. Pizarro. (2023). PyMultiDictionary: v1.2.1. PyPi. https://pypi.org/project/PyMultiDictionary/

---

## How it Works

Here is a thorough explanation of the processing done at the different stages, in case you want to change things up.

### Part 1: Remove Extraneous Data from Kaikki Dictionary

 - The function in `processWordDump.py` takes the raw Kaikki Dictionary file and outputs a new JSON file with a single dictionary object. 
 - The function also takes parameters:
   - `wordsToExclude` - an array of terms which will exclude a word if one of them is found in its definition.
   - `minWordLength` - minimum number of characters a word needs to be included, default 3.
   - `POStoInclude` - a string with the parts of speech to include in the new dictionary. Parts of speech need to be as written in the "pos" keys of the Kaikki dictionary objects and separated by spaces. Default is nouns, verbs, and adjectives. 
   - `ExcludeProfanity` - boolean to control if words with vulgar, derogatory, and offensive tags are removed. Default is True.
 - The following processing is done to return the new dictionary:
   - Remove phrases with spaces
   - Filter to specified parts of speech and words that meet minimum length
   - Filter out word senses with vulgar, derogatory, or offensive tag if `ExcludeProfanity=True`
 - Words are added to the new dictionary with their definitions and related words if present.
     - Related words are filtered if they contain or are contained by the entry word and duplicates are not added to the related words list
     - Only some words in the Kaikki dictionary have related words, and the number of them is hugely variable. They can be type 'synonym', 'hypernym', 'hyponym', 'meronym', 'antonym', or 'related'.
 - Returned dictionary is called the draft dictionary and has the form:
    ```
    "enterprise": {
      "word": "enterprise", 
      "definitions": [
        [
          "noun", 
          "A company, business, organization, or other purposeful endeavor."
        ], 
        [
          "verb", 
          "(intransitive) To undertake an enterprise, or something hazardous or difficult."
        ],
        ...
      ], 
      "related words": [
        ["synonym", "business"], 
        ["hyponym", "corporation"], 
        ["meronym", "factory"],
        ...
      ]
    }
    ```

### Part 2: Apply Frequency Filters to Dictionary

 - The function in `processWordFrequencies.py` takes the draft dictionary file created in Part 1 and creates a new JSON file with a single dictionary, called the rough file.
 - The new dictionary will only include words if they are in the 10,000 most common words are will be sorted from most common to least common. Each word will also have a frequency value. If the language is supported by PyMultiDictionary, then it will attempt to get more synonyms for each word.
 - The following processing is done to return the new dictionary:
   - If `roughFile` is empty, an empty dictionary is created in it.
   - Read in the contents of `roughFile` (empty dictionary if this is the first attempt)
   - For each of the most common 10,000 words retrieved by `wordfreq`, if the word is in the draft dictionary:
     - Check if it's already in `roughFile`
     - Try:
       - Add the frequency rating to the entry and add the entry to the new dictionary object
       - If language suppored by PyMultiDictionary, add new synonyms to related words in the new dictionary -> **this can raise URLError**
     - Except:
       - User chooses whether to try again to get those synonyms
       - If it's skipped then the word won't be added at all 
 - Returned dictionary, written to `roughFile`, is called the rough dictionary and has the form:
    ```
    "enterprise": {
      "word": "enterprise", 
      "definitions": [
        [
          "noun", 
          "A company, business, organization, or other purposeful endeavor."
        ], 
        [
          "verb", 
          "(intransitive) To undertake an enterprise, or something hazardous or difficult."
        ],
        ...
      ], 
      "related words": [
        ["synonym", "business"], 
        ["hyponym", "corporation"], 
        ["meronym", "factory"],
        ...
      ],
      "freqeuncy": 2.39883291901949e-05
    }
    ```

### Part 3: Make Sure There are Enough Related Words

 - The function in `processRelatedWords.py` takes the file created in Part 2 and creates a new JSON file with a dictionary, called the smooth dictionary.
 - The new dictionary will only have words with five or more related words. The definitions for related words will be added if they are not elsewhere in the smooth dictionary.
 - The following processing is done to return the new dictionary:
   - Related words with spaces and below a frequency threshold are filtered
   - Related word list for each word is sorted to have the words in the new dictionary first
   - Loop through each word and each related word
     - If it's in the new dictionary, move on and fetch the definition when needed
     - Otherwise, check the draft dictionary for the word, and add the definition to the related word array if found
     - Otherwise, if not in the draft dicitonary, remove the related word
 - Returned dictionary is called the smooth dictionary and has the form:
    ```
    "enterprise": {
      "word": "enterprise", 
      "definitions": [
        [
          "noun", 
          "A company, business, organization, or other purposeful endeavor."
        ], 
        [
          "verb", 
          "(intransitive) To undertake an enterprise, or something hazardous or difficult."
        ],
        ...
      ], 
      "related words": [
        ["synonym", "business", 0.000363], 
        ["hyponym", "corporation", 3.89e-05], 
        ["meronym", "factory", 3.55e-05, [
          ["noun", "A building or other place where manufacturing takes place."],
          ["noun", "(programming) In a computer program or library, a function, method, etc. which creates an object."],
          ...
        ]],
        ...
      ],
      "freqeuncy": 2.39883291901949e-05
    }
    ```

### Part 4: Putting it All Together

 - The function in `main.py` takes the filepath for the downloaded Kaikki dictionary and the other customizable parameters.
 - It runs each part automatically and creates the new files.

---

## Next Steps

Please feel free to contribute to this repo! Here is my wishlist of features that I'll be prioritising when I continue working on this:

1. [Add more languages!](#more-languages)
2. [Add definitions in native language](#native-definitions)
3. [Find more related words](#more-related-words)

---

### More Languages

The process could theoretically work with many more languages still, as long as it is supported by [wordfreq](https://github.com/rspeer/wordfreq#sources-and-supported-languages). There are still adjustments to make before those dictionaries would come out as expected though.

>For example, the related words in the Korean Kaikki dictionary include [Hanja](https://en.wikipedia.org/wiki/Hanja), sometimes interspersed with Korean characters and sometimes on their own. For my purposes, I wanted only individual related words so that threw a wrench into things. The `add-korean` branch I have going includes a regex to remove the Hanja from the related words.

### Native Definitions

I would like the dictionaries to have definitions in the language of the dictionary, not just in English. 

[Lexicala](https://api.lexicala.com/) has an excellent API which offers definitions for words in many languages, but the usage restrictions are not compatible with this project unless I purchase the data outright. Therefore, it is not be suitable for creating these dictionaries unless I get some funding. I may still use it in my [Talking in Circles](https://github.com/ShoshBeer/talking-circles) project by fetching the definitions directly from the app.

> Sidenote: I reached out to Lexicala to ask a question and they were very responsive and incredibly helpful!

So it's a matter of either finding another resource with definitions in many languages that are free to save, or finding free dictionaries for individual languages and setting the program to run according to the language, or acquiring funding.

### More Related Words

For many languages, the smooth dictionary is empty or has very few words. This is because words with fewer than five related words are filtered out and the current sources for related words are not consistently rich across languages. I'll need to find another way to get related words in different languages for the smooth dictionary to be useful.

 - One option is to look for language specific resources. For example, [datamuse](https://www.datamuse.com/api/) is fantastic for getting related words and supports English and Spanish. 

 - Another option is a resource with support for many languages. This would be ideal. [Lexicala](https://api.lexicala.com/) also has a new synonym functionality, but is not suitable for the same reasons as for native definitions.

 - Another idea I had is if the native definitions are added, then I could extract nouns, verbs, and adjectives from the definitions and add them to the related words. They would likely need more filtering and processing to acquire the base forms of the words. That should be doable with the raw Kaikki dictionary as I believe entries have metadata on the base forms.