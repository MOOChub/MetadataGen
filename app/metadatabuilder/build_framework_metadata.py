from app.helper.load_config import load_framework_conf
from app.framework_handler.framework_data_retriever import get_name_and_description, get_uri_by_name
from .helper import generate_name_and_description_fragment


def build_all_framework_metadata(all_raw_data: list, group: str) -> list:
    """
    Creates a list of all data fragments according to the MOOChub format for data retrieved from frameworks.
    The basis is a list of raw objects with the conceptUrl and the framework together with the group (e.g.
    "educationalAlignment") the list belongs to.

    :param all_raw_data: A list with raw data (framework and conceptUrl).
    :type all_raw_data: list
    :param group: The group the list of data belongs to (e.g. "educationalAlignment")
    :type group: str
    """
    framework_metadata = list()

    for raw_data in all_raw_data:
        build_framework_fragment(raw_data, group)
        framework_metadata.append(raw_data)

    return framework_metadata


def build_framework_fragment(framework_data: dict, group: str) -> None:
    """
    Takes a raw data fragment and enriches it with the mandatory data. It will take parts of the
    data from the respective configuration file connected to the given framework and group. The data
    is modified in the dictionaries via a pass by reference. No return value is needed.

    :param framework_data: A dictionary with the raw data fragment.
    :type framework_data: dict
    :param group: The group the list of data belongs to (e.g. "educationalAlignment")
    :type group: str
    """
    framework = framework_data["educationalFramework"]

    conf = load_framework_conf(framework, group)

    # Fixed data for EducationalAlignment objects
    framework_data["type"] = group[0].upper() + group[1:]  # capitalize() does not work, because it de-capitalizes
    # other words in camelcase.

    # From the config of the selected framework
    framework_data["educationalFrameworkVersion"] = conf["VERSION"]
    framework_data["url"] = conf["URL"]

    target_uri = framework_data.get("targetUrl")

    # The targetUrl is an optional attribute, it does not have to be provided, this will look up the
    # uri by name
    if not target_uri:
        name = framework_data["name"][0].get("name")  # TODO: what if there is no name? Find solution!
        target_uri = get_uri_by_name(name, group, framework)
        framework_data["targetUrl"] = target_uri

    # Data from the framework CSV
    additional_data = get_name_and_description(framework, group, target_uri)

    for k, v in generate_name_and_description_fragment(additional_data, conf).items():
        framework_data[k] = v
