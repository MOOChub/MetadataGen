import traceback

from app.framework_handler.framework_data_retriever import find_top_level_entries, find_sub_entries


test_data = {
    "teaches": "ESCO",
    "educationalAlignment": "ISCED-F",
    "educationalLevel": "DigComp"
}


def get_next_entries(group, framework, uri):
    sub_entries = find_sub_entries(group, framework, uri)
    try:
        if sub_entries.empty:
            return True

        selected_entry = sub_entries.iloc[0]["narrowerconcept"]
        selected_entry = eval(selected_entry)

        if len(selected_entry) == 0:
            return True

        return get_next_entries(group, framework, selected_entry[0])
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        return False


def run_test():
    res = dict()
    for group, framework in test_data.items():
        top_level_entries = find_top_level_entries(group, framework)

        selected_entry = top_level_entries.iloc[0]["uri"]

        test_passed = get_next_entries(group, framework, selected_entry)
        res[framework] = test_passed

    return res


print(run_test())
