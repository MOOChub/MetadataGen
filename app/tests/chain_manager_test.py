import json
from pathlib import Path
from app.llm_support.chain_manager import execute_chain
from pprint import pprint


path_valid = Path("test_data/test_input_suggestion_valid.json")


def test_llm(path):
    with open(path, "r") as f:
        test_data = json.loads(f.read())

    name = test_data["name"]
    desc = test_data["description"]

    query = name + ". " + desc

    res = execute_chain("DigComp", query)

    pprint(res)


test_llm(path_valid)
