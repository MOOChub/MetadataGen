import requests
from pathlib import Path
import json

url = "http://127.0.0.1:5000/suggestion"

path_test_data_valid = Path("test_data/test_input_full_suggestion_valid.json")

#print(test_data_valid.exists())
with open(path_test_data_valid, "r") as f:
    test_data_valid = json.loads(f.read())

#print(test_data_valid)

res_valid = requests.post(url, json=test_data_valid)

print(res_valid)
print(json.loads(res_valid.json()))



