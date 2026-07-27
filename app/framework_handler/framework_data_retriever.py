import json
import pandas as pd
from pandas import DataFrame
from app.helper.paths import FRAMEWORK_ROOT
import os


def get_name_and_description(framework: str, group: str, uri: str):
    """
    Extracts and returns a name and a description of a given entry of a specified framework.

    :param framework: The framework the entry is from.
    :type framework: str
    :param group: The group the framework belongs to (e.g. educationalAlignment).
    :type group: str
    :param uri: The URI of the entity as an unambiguous identifier.
    :type uri: str
    :return: The name and the description of the entry.
    :rtype: dict
    """

    data = get_full_framework(group, framework)

    return {
        "name": data[data["uri"] == uri]["name"].item(),
        "description": data[data["uri"] == uri]["description"].item()
    }


def get_full_framework(group: str, framework: str) -> DataFrame:
    """
    Returns the specified framework as a pandas DataFrame.

    :param group: The group the framework belongs to.
    :type group: str
    :param framework: The framework to be returned.
    :type framework: str
    :return: The complete framework.
    :rtype: pandas.DataFrame
    """

    path = (
        FRAMEWORK_ROOT /
        group /
        framework
    )

    file = [file for file in os.listdir(path) if file[-4:] == ".csv"][0]

    path = (
            path /
            file
    )

    return pd.read_csv(path, dtype=str)


def get_uri_by_name(name, group, framework):
    data = get_full_framework(group, framework)
    data = data[data["name"] == name]
    max_level = data["level"].max()

    return data[data["level"] == max_level]["uri"].item()


def get_ed_level_uri_by_name(name, framework: str) -> str:
    data = get_full_framework("educationalLevel", framework)
    name = f"Level {name}"
    return data[data["name"].str.contains(name)]["uri"].item()


def find_top_level_entries(group: str, framework: str):
    data = get_full_framework(group, framework)

    return data[data["level"] == "1"]


def find_sub_entries(group: str, framework: str, uri: str):
    data = get_full_framework(group, framework)
    sub_entries = json.loads(data[data["uri"] == uri]["narrowerconcept"].item().replace("'", '"'))  # TODO: eval instead?

    return data[data["uri"].isin(sub_entries)]
