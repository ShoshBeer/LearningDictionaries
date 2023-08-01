import json

pt_file = open('dictionaries/pt/pt_smooth_dict.json', 'r', encoding="utf-8")
pt = json.load(pt_file)
pt_file.close()

print(len(pt))