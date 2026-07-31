import pandas as pd
from pandas import DataFrame
from app.helper.paths import FRAMEWORK_ROOT
import os


def get_description(framework: str, group: str, uri: str) -> str | None:
    """
    Extracts and returns a name and a description of a given entry of a specified framework.

    :param framework: The framework the entry is from.
    :type framework: str
    :param group: The group the framework belongs to (e.g. educationalAlignment).
    :type group: str
    :param uri: The URI of the entity as an unambiguous identifier.
    :type uri: str
    :return: The description of the entry.
    :rtype: str
    """
    if uri:
        data = get_full_framework(group, framework)

        description = data[data["uri"] == uri]["description"].item()
        if description and type(description) != float:
            return description
    return None


def get_full_framework(group: str, framework: str) -> DataFrame:
    """
    Returns the specified framework as a pandas DataFrame.

    :param group: The group the framework belongs to.
    :type group: str
    :param framework: The framework to be returned.
    :type framework: str
    :return: The complete framework.
    :rtype: DataFrame
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


def get_uri_by_name(name: str, group: str, framework: str) -> str | None:
    """
    Return the URI of a framework entry identified by its name. The framework
    is searched by the name and only the entry with the highest level is returned
    in case that thee are several entries with the same name. If there is no URI
    available None is returned.

    :param name: The name of the entry.
    :type name: str
    :param group: The attribute the entry belongs to.
    :type group: str
    :param framework: The framework the entry belongs to.
    :type framework: str
    :return: The URI of the entry or None if no URI is available.
    :rtype: str | None
    """
    data = get_full_framework(group, framework)
    data = data[data["name"] == name]
    max_level = data["level"].max()

    uri = data[data["level"] == max_level]["uri"].item()
    if type(uri) != float:
        return uri
    return None


def find_top_level_entries(group: str, framework: str) -> DataFrame:
    """
    Find all level 1 entries of a given framework. This is needed to start the
    dropdown menu of the frameworks on the user interface.

    :param group: The attribute the entries belong to.
    :type group: str
    :param framework: The framework the entries belong to.
    :type framework: str
    :return: A DataFrame containing all level 1 entries of a given framework.
    :rtype: DataFrame
    """
    data = get_full_framework(group, framework)

    return data[data["level"] == "1"]


def find_sub_entries(group: str, framework: str, uri: str) -> DataFrame:
    """
    Find all sub-entries to a given entry. This is important to build the dropdown
    menu for the user interface dynamically.

    :param group: The attribute the entries belong to.
    :type group: str
    :param framework: The framework the entries belong to.
    :type framework: str
    :param uri: The URI of the entry as unique identifier within the framework.
    :return: A DataFrame with all sub-entries for a given entry.
    :rtype: DataFrame
    """
    data = get_full_framework(group, framework)
    sub_entries = eval(data[data["uri"] == uri]["narrowerconcept"].item())

    return data[data["uri"].isin(sub_entries)]
