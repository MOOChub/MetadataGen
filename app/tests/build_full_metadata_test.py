import traceback

from app.metadatabuilder.build_full_metadata import build_metadata
from pathlib import Path
import json

path_valid_with_target_url = Path("test_data/input_metadata_formatting_valid_with_targetUrl.json")
path_valid_no_target_url = Path("test_data/input_metadata_formatting_valid_no_targetURL.json")
path_invalid_no_framework = Path("test_data/input_metadata_formatting_invalid_no_framework.json")
path_invalid_no_creator = Path("test_data/input_metadata_formatting_invalid_no_creator.json")


paths = {
    "valid_with_url": path_valid_with_target_url,
    "valid_no_url": path_valid_no_target_url,
    "invalid_no_framework": path_invalid_no_framework,
    "invalid_no_creator": path_invalid_no_creator
}


def run_tests():
    results = dict()
    for test, data_path in paths.items():
        with open(data_path, "r") as f:
            test_data = json.loads(f.read())

        try:
            build_metadata(test_data)
            results[test] = "passed"
        except Exception as e:
            print(e)
            print(traceback.print_exc())
            results[test] = "failed"

    return results


print(run_tests())
