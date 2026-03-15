import json

data = {}

with open("ram_data_page1.json", "r", encoding='utf-8') as file:
    data = json.load(file)

#print(data)
print(type(data["data"][0][0]))

