def parse_suggestion(raw_suggestion: tuple[list, str]) -> list:
    """
    Parses the suggestion received from the similarity search for further processing with
    the metadata_builder module.

    :param raw_suggestion: A tuple that contains a list with the raw suggestions and the
    framework the suggestions were made from.
    :return: The parsed suggestions ready to be processed with the metadata_builder.
    :rtype: list
    """
    framework = raw_suggestion[1]
    raw_suggestion = [suggestion[0] for suggestion in raw_suggestion[0]]
    suggestions = list()

    for suggestion in raw_suggestion:
        temp = dict()
        temp["name"] = suggestion["name"]
        temp["targetUrl"] = suggestion["uri"]
        temp["educationalFramework"] = framework

        suggestions.append(temp)

    return suggestions
