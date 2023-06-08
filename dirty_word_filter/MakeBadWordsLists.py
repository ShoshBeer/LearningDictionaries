import json

with open("DirtyWords.json", "r", encoding="utf-8") as f:
  DirtyDictionary = {}
  data = json.load(f)
  for word in data["RECORDS"]:
    if word["language"] in DirtyDictionary:
      DirtyDictionary[word["language"]].append(word["word"])
    else:
      DirtyDictionary[word["language"]] = [word["word"]]

with open("dirty_dictionary.json", "w", encoding="utf-8") as f:
  json.dump(DirtyDictionary, f)
