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

def wordNotInList(word, listOfWords, nested=False):
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
  # for wordFromList in listOfWords:
  #   if word.casefold() == wordFromList.casefold():
  #     return False
  #   else:
  #     continue
  
  # return word.casefold()

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

  print(wordNotInList(testWord1, testList1))
  print(wordNotInList(testWord1, testList2))
  print(wordNotInList(testWord1, testList3))
  print(wordNotInList(testWord1, testList4))
  print(wordNotInList(testWord1, testList5))

  # wordInString
  testSentence1 = "Don't look at my bUtt" # Expect True
  testSentence2 = "Don't look at my butt./" # Expect True
  testSentence3 = "sdfgjbegkjberesgrskgSGSTHWRT" # Expect False
  testSentence4 = "many buttresses" # Expect False
  testSentence5 = "BUT T S" # Expect False


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

