import json

with open('../aaa.txt') as json_file:
    data = json.load(json_file)
print (data)
print (data['consumer_key'])