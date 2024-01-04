import json

with open('logic_playground/structure.json', "r", encoding="utf-8") as f:
  bad_words = []
  good_words = []
  for line in f:
    data = json.loads(line)
    for sense in range(len(data["senses"])):
      if "tags" in data["senses"][sense] and any([x in data["senses"][sense]["tags"] for x in ["derogatory", "offensive", "vulgar"]]):
        bad_words.append(data["senses"][sense]["raw_glosses"])
      else:
        good_words.append(data["senses"][sense]["raw_glosses"])

print(f'Good words: {good_words}')
print(f'Bad words: {bad_words}')