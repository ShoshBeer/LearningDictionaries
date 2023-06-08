import wordfreq as wf
import json
import random
import re

'''
Test regex to remove characters in brackets from related words
'''
test = re.findall('[^\s()]+(?![^(]*\))', "민주화(民主化)하다")
test1 = re.match('[^()]*(?![^(]*\))', "민주 열사(民主烈士)").group()
test2 = re.match('[^()]*(?<! )', "조선어 (朝鮮語) (joseoneo)").group()
print(test2)


'''
Test excluded words with german word whose defs didn't get excluded

excluded = [
            "obsolete", "rare", "archaic", 
            "regional", "dialectal",
            "abbreviation", "initialism", "colloquial", "slang", 
            "simple past", "past participle", 
            "simple present", "present participle", 
            "future tense", "imperative", "first-person", "third-person",
            "plural of", "plural future", "singular present",
            "genitive", "dative", "accusative", "nominative", "all-case",
            "feminine", "masculine", "neuter", "all-gender",
            "misspelling", "alternative form", "alternative spelling", "defective spelling", "alternative letter", 
            "script ", "greek", "phonetic"
          ]

habe = {"pos": "verb", "head_templates": [{"name": "head", "args": {"1": "de", "2": "verb form"}, "expansion": "habe"}], "word": "habe", "lang": "German", "lang_code": "de", "sounds": [{"ipa": "/ˈhaːbə/"}, {"audio": "De-habe.ogg", "text": "Audio", "ogg_url": "https://upload.wikimedia.org/wikipedia/commons/a/ae/De-habe.ogg", "mp3_url": "https://upload.wikimedia.org/wikipedia/commons/transcoded/a/ae/De-habe.ogg/De-habe.ogg.mp3"}], "categories": [], "senses": [{"raw_glosses": ["first-person singular present"], "glosses": ["inflection of haben:\n## first-person singular present\n## first/third-person singular subjunctive I\n## singular imperative", "first-person singular present"], "form_of": [{"word": "haben"}], "tags": ["first-person", "form-of", "present", "singular"], "id": "habe-de-verb-zFFJjG6g"}, {"raw_glosses": ["first/third-person singular subjunctive I"], "glosses": ["inflection of haben:\n## first-person singular present\n## first/third-person singular subjunctive I\n## singular imperative", "first/third-person singular subjunctive I"], "form_of": [{"word": "haben"}], "tags": ["first-person", "form-of", "singular", "subjunctive-i", "third-person"], "id": "habe-de-verb-IpV~wC1o"}, {"raw_glosses": ["singular imperative"], "glosses": ["inflection of haben:\n## first-person singular present\n## first/third-person singular subjunctive I\n## singular imperative", "singular imperative"], "form_of": [{"word": "haben"}], "tags": ["form-of", "imperative", "singular"], "id": "habe-de-verb-I4Xf~vWC"}]}

for sense in range(len(habe["senses"])):
  if "raw_glosses" in habe["senses"][sense]:
    if not any([x in habe["senses"][sense]["raw_glosses"][0].casefold() for x in excluded]):
      print([habe["pos"], habe["senses"][sense]["raw_glosses"][0]])
    else:
      print(f'Excluded {habe["senses"][sense]["raw_glosses"][0]}')
'''

'''
Test removing hebrew words with tags vulgar, derogatory, or offensive

data = {"pos": "noun", "head_templates": [{"name": "he-noun", "args": {"pl": "שַׁרְמוּטוֹת", "wv": "שַׁרְמוּטָה", "g": "f", "tr": "sharmúta"}, "expansion": "שַׁרְמוּטָה • (sharmúta) f (plural indefinite שַׁרְמוּטוֹת)"}], "forms": [{"form": "שַׁרְמוּטָה", "tags": ["canonical"]}, {"form": "sharmúta", "tags": ["romanization"]}, {"form": "שַׁרְמוּטוֹת", "tags": ["indefinite", "plural"]}], "etymology_text": "From Arabic شَرْمُوطَة (šarmūṭa).", "etymology_templates": [{"name": "bor", "args": {"1": "he", "2": "ar", "3": "شَرْمُوطَة"}, "expansion": "Arabic شَرْمُوطَة (šarmūṭa)"}], "word": "שרמוטה", "lang": "Hebrew", "lang_code": "he", "categories": [], "senses": [{"raw_glosses": ["(derogatory, vulgar) whore, slut (promiscuous woman)"], "synonyms": [{"word": "זונה"}], "glosses": ["whore, slut (promiscuous woman)"], "tags": ["derogatory", "vulgar"], "id": "שרמוטה-he-noun-d2cwuT-J", "categories": []}, {"raw_glosses": ["(derogatory, vulgar) scumbag (despicable person)"], "glosses": ["scumbag (despicable person)"], "tags": ["derogatory", "vulgar"], "id": "שרמוטה-he-noun-6KPmYyG3", "categories": []}]}

data = {"pos": "noun", "head_templates": [{"name": "he-noun", "args": {"wv": "תַּחַת", "g": "m", "tr": "tákhat", "pat": "קֶטֶל"}, "expansion": "תַּחַת • (tákhat) m [pattern: קֶטֶל]"}], "forms": [{"form": "תַּחַת", "tags": ["canonical"]}, {"form": "tákhat", "tags": ["romanization"]}], "etymology_text": "Root\n ת־ח־ת (t-ḥ-t)\nRelated to Arabic تَحْتَ (taḥta), Ge'ez ታሕተ (taḥtä), Ugaritic 𐎚𐎈𐎚 (tḥt /taḥta/).", "etymology_templates": [{"name": "l", "args": {"1": "he", "2": "ת־ח־ת", "tr": "t-ḥ-t"}, "expansion": "ת־ח־ת (t-ḥ-t)"}, {"name": "catlangname", "args": {"1": "he", "2": "terms belonging to the root ת־ח־ת"}, "expansion": ""}, {"name": "HE root", "args": {"1": "תחת"}, "expansion": "Root\n ת־ח־ת (t-ḥ-t)"}, {"name": "cog", "args": {"1": "ar", "2": "تَحْتَ"}, "expansion": "Arabic تَحْتَ (taḥta)"}, {"name": "cog", "args": {"1": "gez", "2": "ታሕተ"}, "expansion": "Ge'ez ታሕተ (taḥtä)"}, {"name": "cog", "args": {"1": "uga", "2": "𐎚𐎈𐎚", "ts": "taḥta"}, "expansion": "Ugaritic 𐎚𐎈𐎚 (tḥt /taḥta/)"}], "sounds": [{"ipa": "/ˈta.χat/", "tags": ["Modern-Israeli-Hebrew"]}, {"ipa": "/ˈta.xas/", "tags": ["Ashkenazi-Hebrew"]}, {"ipa": "[ˈta.xəs]", "tags": ["Ashkenazi-Hebrew"]}, {"ipa": "/ˈta.ħat/", "note": "Sephardi Hebrew"}, {"ipa": "/ˈtæ.ħæθ/", "tags": ["Yemenite-Hebrew"]}, {"ipa": "/ˈta.ħaθ/", "tags": ["Tiberian-Hebrew"]}], "word": "תחת", "lang": "Hebrew", "lang_code": "he", "derived": [{"roman": "khor tákhat", "word": "חור תחת", "_dis1": "0 0 0"}, {"roman": "khor tákhat", "word": "חֹר תַּחַת", "_dis1": "0 0 0"}], "senses": [{"raw_glosses": ["bottom"], "glosses": ["bottom"], "id": "תחת-he-noun-vpt2B-Bw"}, {"raw_glosses": ["underside"], "glosses": ["underside"], "id": "תחת-he-noun-9DbW-Fsr", "categories": [{"name": "Hebrew prepositions", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "9 12 9 11 16 18 20 5"}, {"name": "Hebrew terms belonging to the root ת־ח־ת", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "0 30 0 0 19 8 12 31"}]}, {"raw_glosses": ["(vulgar) butt, ass"], "glosses": ["butt, ass"], "tags": ["vulgar"], "id": "תחת-he-noun-IZn~iLSb", "categories": []}]}

data = {"pos": "noun", "head_templates": [{"name": "he-noun", "args": {"g": "f", "wv": "בֵּיצָה", "tr": "betzá", "pl": "בֵּיצִים", "cons": "בֵּיצַת", "plcons": "בֵּיצֵי"}, "expansion": "בֵּיצָה • (betzá) f (plural indefinite בֵּיצִים, singular construct בֵּיצַת־, plural construct בֵּיצֵי־)"}], "forms": [{"form": "בֵּיצָה", "tags": ["canonical"]}, {"form": "betzá", "tags": ["romanization"]}, {"form": "בֵּיצִים", "tags": ["indefinite", "plural"]}, {"form": "בֵּיצַת־", "tags": ["construct", "singular"]}, {"form": "בֵּיצֵי־", "tags": ["construct", "plural"]}], "etymology_number": 1, "etymology_text": "Root\n ב־ו־ץ (b-w-ṣ)\nCognate with Arabic بَيْض (bayḍ) and Classical Syriac ܒܝܥܬܐ (bēʿṯā).", "etymology_templates": [{"name": "l", "args": {"1": "he", "2": "ב־ו־ץ", "tr": "b-w-ṣ"}, "expansion": "ב־ו־ץ (b-w-ṣ)"}, {"name": "catlangname", "args": {"1": "he", "2": "terms belonging to the root ב־ו־ץ"}, "expansion": ""}, {"name": "HE root", "args": {"1": "בוץ"}, "expansion": "Root\n ב־ו־ץ (b-w-ṣ)"}, {"name": "cog", "args": {"1": "ar", "2": "بَيْض"}, "expansion": "Arabic بَيْض (bayḍ)"}, {"name": "cog", "args": {"1": "syc", "2": "ܒܝܥܬܐ", "tr": "bēʿṯā"}, "expansion": "Classical Syriac ܒܝܥܬܐ (bēʿṯā)"}], "word": "ביצה", "lang": "Hebrew", "lang_code": "he", "derived": [{"roman": "beytsá mekushkéshet", "word": "ביצה מקושקשת", "_dis1": "0 0"}, {"roman": "beytsá mekushkéshet", "word": "בֵּיצָה מְקֻשְׁקֶשֶׁת", "_dis1": "0 0"}, {"roman": "magén beytsím", "word": "מָגֵן בֵּיצִים", "_dis1": "0 0"}], "senses": [{"raw_glosses": ["egg"], "examples": [{"text": "אני צריך ללכת לקנות ביצים.", "english": "I need to go buy eggs.", "type": "example"}], "glosses": ["egg"], "id": "ביצה-he-noun-NHB8P0Df", "categories": [{"name": "Hebrew terms belonging to the root ב־צ־ץ", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "12 44 44"}, {"name": "Eggs", "kind": "topical", "parents": ["Foods", "List of sets", "Food and drink", "All sets", "All topics", "Fundamental"], "source": "w+disamb", "orig": "he:Eggs", "langcode": "he", "_dis": "54 37 10"}]}, {"raw_glosses": ["(slang, in the plural, vulgar) testicles, balls (referring to anatomy, bravery or general self-assuredness)"], "examples": [{"text": "יש לו ביצים גדולות שהוא אוהב להראות לכולם.", "english": "He has big testicles that he loves to show to everyone.", "type": "example"}], "glosses": ["testicles, balls (referring to anatomy, bravery or general self-assuredness)"], "tags": ["in-plural", "slang", "vulgar"], "id": "ביצה-he-noun-qLRoac1R", "categories": [{"name": "Hebrew feminine nouns with plurals ending in ־ים", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "30 70"}, {"name": "Hebrew terms belonging to the root ב־ו־ץ", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "21 79"}, {"name": "Hebrew terms belonging to the root ב־צ־ץ", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "12 44 44"}, {"name": "Hebrew terms in the pattern קִטְלָה", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "10 47 43"}]}]}

for sense in range(len(data["senses"])):
  if "tags" in data["senses"][sense] and any([x in data["senses"][sense]["tags"] for x in ["derogatory", "offensive", "vulgar"]]):
    print(f'Definition {data["senses"][sense]["raw_glosses"][0]} for word {data["word"]} is offensive, derogatory, or vulgar.')
  else:
    print(f'Definition {data["senses"][sense]["raw_glosses"][0]} for word {data["word"]} is okay.')
'''

'''
Test writing words to file, error handling, and continuing from a file

words = {"that": {"word": "that", "definitions": [["noun", "(philosophy) Something being indicated that is there; one of those."]], "related words": [["relate", "which"]], "frequency": 0.010232929922807542}}
word1 = '"that": {"word": "that", "definitions": [["noun", "(philosophy) Something being indicated that is there; one of those."]], "related words": [["relate", "which"]], "frequency": 0.010232929922807542}'

word2 = '"you": {"word": "you", "definitions": [["verb", "(transitive) To address (a person) using the pronoun you (in the past, especially to use you rather than thou, when you was considered more formal)."]], "related words": [], "frequency": 0.009549925860214359}'

wordsToAdd = [{"word": "this"}, {"word": "are"}, {"word": "abide"}, {"word": "arise"}, {"word": "attend"}]

def readJson():
  # Starting with a JSON object in the file
  file = open('test-write-json.json', 'r+', encoding="utf-8")
  if len(file.readline()) == 0:
    json.dump({}, file)
  file.close()
  
  # Now this is buffered content I can work with
  file = open('test-write-json.json', 'r', encoding="utf-8")
  data = json.load(file)
  file.close()

   # Now I work with the content
  for word in wordsToAdd:
    while True:
      failSometimes = random.random()
      try:
        if failSometimes < 0.2:
          raise KeyError
        
        if word["word"] in data:
          break

        print(f"Adding word: {word['word']}")
        data[word["word"]] = word
        break

      except KeyError:
        print(f'Failed to get synonyms for {word["word"]}')
        ans = input("(y/n) Keep trying? ")
        if ans == 'n':
          break

  # Now I write the stuff I just did to the file (I update the object with my new object)
  file = open('test-write-json.json', 'w+', encoding="utf-8")
  json.dump(data, file)
  file.close()

  return None

readJson()
'''

'''
Added more excluded words and reprocessed the German smooth dict

wordsToExclude = [
            "obsolete", "rare", "archaic", 
            "regional", "dialectal",
            "abbreviation", "initialism", "colloquial", "slang", 
            "simple past", "past participle", 
            "simple present", "present participle", 
            "future tense", "imperative", "first-person", "third-person",
            "plural of", "plural future", "singular present",
            "genitive", "dative", "accusative", "nominative", "all-case",
            "feminine", "masculine", "neuter", "all-gender",
            "misspelling", "alternative form", "alternative spelling", "defective spelling", "alternative letter", 
            "script ", "greek", "phonetic"
          ]
langCode = 'de'
with open('smooth_dict_de.json', "r", encoding="utf-8") as f:
  extraSmoothDict = {}
  wordsToProccess = json.load(f)
  for word in wordsToProccess:
    extraSmoothDict[word] = wordsToProccess[word]
    extraSmoothDict[word]["definitions"] = list(filter(filterBadDefs, extraSmoothDict[word]["definitions"]))

    if len(extraSmoothDict[word]["definitions"]) == 0:
      del extraSmoothDict[word]
'''

# test_freq_function_no_RW_filter.json: No RW: 954, 1-4 RW: 502, 5+ RW: 5161.

