from app.framework_handler.framework_data_retriever import get_ed_level_uri_by_name


def parse_chain_output(chain_output: str, framework: str) -> dict:
    """
    Parses the output of the langchain. The LLM generated text is converted into
    a dictionary containing the separated and preprocessed data for the keywords
    and the educational level suggestion. The preprocessed data is ready-to-use
    for the metadata_builder module.

    :param chain_output: The raw output from the langchain as a pure text.
    :type chain_output: str
    :param framework: The framework for the educational level suggestion.
    :type framework: str
    :return: The preprocessed metadata ready to be further enriched with the
    metadata_builder module.
    :rtype: dict
    """
    parsed_output = dict()

    chain_output = chain_output.split("\n")
    chain_output = [line for line in chain_output if "=" in line]
    chain_output = {line.split(" = ")[0]: line.split(" = ")[1] for line in chain_output}

    keywords = chain_output.get("keywords")
    if keywords:
        keywords = eval(keywords)
        parsed_output["keywords"] = keywords

    ed_level = chain_output.get("educationalLevel")
    if ed_level:
        uri = get_ed_level_uri_by_name(ed_level, framework)

        ed_level = dict()
        ed_level["conceptUrl"] = uri
        ed_level["educationalFramework"] = framework

        parsed_output["educationalLevel"] = [ed_level]

    return parsed_output
