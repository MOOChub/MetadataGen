import traceback
from pathlib import Path
from app.suggestion_management.suggestion_manager import generate_full_suggestion
import json

paths = {
    "path_valid_full": Path("test_data/test_input_full_suggestion_no_llm_valid.json"),
    "path_invalid_full": Path("test_data/test_input_full_suggestion_no_llm_invalid.json"),
    "path_valid_full_llm": Path("test_data/test_input_full_suggestion_valid.json"),
    "path_invalid_full_llm": Path("test_data/test_input_full_suggestion_invalid.json")
}


def run_test():
    res = dict()

    raw_data = dict()

    for test, path in paths.items():
        with open(path, "r") as f:
            raw_data[test] = json.loads(f.read())

    for test, data in raw_data.items():
        try:
            generate_full_suggestion(data)
            res[test] = True
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            res[test] = False

    return res


print(run_test())
