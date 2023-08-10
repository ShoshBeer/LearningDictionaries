# If space, skip
# If length, skip
# If not POS, skip
# If word not added, add (certain key-values)
# For word senses:
#   If profane, skip
#   If raw_glosses has no words to exlude, add def
#   If no raw_glosses and glosses has no words to exlude, add def
#   If no overlap with word or RW, add RW
# If no defs, delete word
import re

def wordNotInList(word, listOfWords, targetWord=None, nested=False, excludedChars=[]):
  if targetWord and word.casefold() == targetWord.casefold():
    return False
  if any(excludedChar in word for excludedChar in excludedChars):
    return False
  if nested:
    if any(word.casefold() == wordFromList[1].casefold() for wordFromList in listOfWords):
      return False
    else:
      return word.casefold()
  else:
    if any(word.casefold() == wordFromList.casefold() for wordFromList in listOfWords):
      return False
    else:
      return word.casefold()
    
def findRelationships(dictionaryWithRelationships):
  relationships = set(["synonyms", "holonyms", "hypernyms", "hyponyms", "meronyms", "antonyms", "troponyms", "related"])
  dictionaryKeys = set([*dictionaryWithRelationships])
  return list(relationships.intersection(dictionaryKeys))


def wordInString(word, sentence):
  wordList = re.findall(r'\w+', sentence)
  for wordFromSentence in wordList:
    if word.casefold() == wordFromSentence.casefold():
      return True
    else:
      continue
  
  return False
    

if __name__ == "__main__":

  # wordNotInList
  testWord1 = "butt"
  testList1 = ["nutty", "putty", "butty"] # Expect butt
  testList2 = ["no", "words", "here"] # Expect butt
  testList3 = ["here", "butt", "booty"] # Expect False
  testList4 = ["here", "bUtt", "booty"] # Expect False
  testList5 = ["one", "butt./"] # Expect butt

  # print("Testing wordNotInList():")
  # print(wordNotInList(testWord1, testList1, excludedChars=['-', ' ']))
  # print(wordNotInList(testWord1, testList2, excludedChars=['-', ' ']))
  # print(wordNotInList(testWord1, testList3, excludedChars=['-', ' ']))
  # print(wordNotInList(testWord1, testList4, excludedChars=['-', ' ']))
  # print(wordNotInList(testWord1, testList5, excludedChars=['-', ' ']))

  # findRelationships
  exampleWordEntry = {
    "pos": "noun", "head_templates": [{"name": "he-noun", "args": {"wv": "בָּרָד", "tr": "barád", "g": "m", "cons": "בְּרַד", "pl": "בְּרָדִים", "plcons": "ברדי", "1": "", "pat": "קָטָל"}, "expansion": "בָּרָד • (barád) m (plural indefinite בְּרָדִים, singular construct בְּרַד־, plural construct ברדי־) [pattern: קָטָל]"}], "forms": [{"form": "בָּרָד", "tags": ["canonical"]}, {"form": "barád", "tags": ["romanization"]}, {"form": "בְּרָדִים", "tags": ["indefinite", "plural"]}, {"form": "בְּרַד־", "tags": ["construct", "singular"]}, {"form": "ברדי־", "tags": ["construct", "plural"]}], "etymology_text": "Root\n ב־ר־ד (b-r-d)\nCompare Aramaic בַּרְדָא (barḏā), Arabic بَرَد (barad), Ge'ez በረድ (bäräd).", "etymology_templates": [{"name": "l", "args": {"1": "he", "2": "ב־ר־ד", "tr": "b-r-d"}, "expansion": "ב־ר־ד (b-r-d)"}, {"name": "catlangname", "args": {"1": "he", "2": "terms belonging to the root ב־ר־ד"}, "expansion": ""}, {"name": "HE root", "args": {"1": "ברד"}, "expansion": "Root\n ב־ר־ד (b-r-d)"}, {"name": "cog", "args": {"1": "arc", "2": "בַּרְדָא", "tr": "barḏā"}, "expansion": "Aramaic בַּרְדָא (barḏā)"}, {"name": "cog", "args": {"1": "ar", "2": "بَرَد"}, "expansion": "Arabic بَرَد (barad)"}, {"name": "cog", "args": {"1": "gez", "2": "በረድ"}, "expansion": "Ge'ez በረድ (bäräd)"}], "word": "ברד", "lang": "Hebrew", "lang_code": "he", "hypernyms": [{"roman": "géshem", "word": "גֶּשֶׁם", "_dis1": "0 0"}, {"roman": "matár", "word": "מָטָר", "_dis1": "0 0"}, {"roman": "shéleg", "word": "שֶׁלֶג", "_dis1": "0 0"}], "holonyms": [{"word": "מִשְׁקָע", "_dis1": "0 0"}], "senses": [{"raw_glosses": ["(countable and uncountable) hail"], "examples": [{"text": "רֵעַי שְׁתוּ עִמִּי עֲלֵי-אֶרֶץ \\ גֻּשְׁמַהּ וְעַל-יַעַר אֲשֶׁר בָּרָד ⁋ יַיִן כְּמוֹ-אֹדֶם בְּכוֹס שֹׁהַם \\ אוֹ אֵשׁ מְלֻקָּחָה בְּתוֹךְ בָּרָד.", "ref": "c. 1055 – 1138, Moses ibn Ezra, רעי שתו עמי עלי ארץ", "type": "example"}], "glosses": ["hail"], "tags": ["countable", "uncountable"], "id": "ברד-he-noun-H2Y5qKUc", "categories": [{"name": "Hebrew terms belonging to the root ב־ר־ד", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "52 48"}, {"name": "Weather", "kind": "topical", "parents": ["Atmosphere", "Nature", "All topics", "Fundamental"], "source": "w+disamb", "orig": "he:Weather", "langcode": "he", "_dis": "80 20"}]}, {"raw_glosses": ["a snow cone"], "glosses": ["a snow cone"], "id": "ברד-he-noun-DTsyhrRU", "categories": [{"name": "Hebrew terms belonging to the root ב־ר־ד", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "52 48"}, {"name": "Hebrew terms in the pattern קָטָל", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "36 64"}]}]
  }
  exampleSense1 = {
    "raw_glosses": ["quick, agile, nimble"], "synonyms": [{"word": "מָהִיר"}], "antonyms": [{"word": "אִיטִּי"}], "glosses": ["quick, agile, nimble"], "id": "זריז-he-adj-YgbmSaSZ", "categories": [{"name": "Hebrew terms belonging to the root ז־ר־ז", "kind": "other", "parents": [], "source": "w+disamb", "_dis": "62 38"}]
  }
  exampleSense2 = {
    "raw_glosses": ["a rebellion, insurrection, mutiny, an uprising"], "glosses": ["a rebellion, insurrection, mutiny, an uprising"], "id": "מרד-he-noun-Sd5pkJ8u", "synonyms": [{"sense": "rebellion", "roman": "hitkomemút", "word": "הִתְקוֹמְמוּת"}, {"sense": "rebellion", "roman": "méri", "word": "מֶרִי"}], "hyponyms": [{"roman": "intifáda", "english": "intifada", "word": "אִנְתִּיפָדָה"}]
  }

  exampleW = findRelationships(exampleWordEntry) # Expect ["holonyms", "hypernyms"]
  example1 = findRelationships(exampleSense1) # Expect ["synonyms", "antonyms"]
  example2 = findRelationships(exampleSense2) # Expect ["synonyms", "hyponyms"]

  # print(example2, example1[0], example1[1])
  # print(example1[0])
  # print(example1[1])

  # wordInString
  testSentence1 = "Don't look at my bUtt" # Expect True
  testSentence2 = "Don't look at my butt./" # Expect True
  testSentence3 = "sdfgjbegkjberesgrskgSGSTHWRT" # Expect False
  testSentence4 = "many buttresses" # Expect False
  testSentence5 = "BUT T S" # Expect False

  # print("Testing wordInString():")
  # print(wordInString(testWord1, testSentence1))
  # print(wordInString(testWord1, testSentence2))
  # print(wordInString(testWord1, testSentence3))
  # print(wordInString(testWord1, testSentence4))
  # print(wordInString(testWord1, testSentence5))

  # POS = 'Noun. verb adj'
  # parts = ["noun", "verb", "adjective", "adv", "intj"]
  # for part in parts:
  #   if part in POS.casefold():
  #     print("Include word")
  #   else:
  #     print("exclude word")

  testdict = {
    "pretty": {"syn": "cute", "ant": "ugly", "freq": 345},
    "icing": {"syn": "bonus", "holo": "cake", "yummy": True, "hyper": "chocolate"}
  }

  relationships = ["syn", "ant", "holo", "hyper", "hypo", "mero"]

  # for word in testdict:
  #   RWs = []
  #   relations = (relationship for relationship in relationships if relationship in testdict[word])
  #   for relation in relations:
  #     RWs.append(testdict[word][relation])
  #   print(RWs)

