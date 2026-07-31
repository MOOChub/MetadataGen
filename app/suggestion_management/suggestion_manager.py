from app.suggestion_engine.similarity_search import search_frameworks
from app.suggestion_engine.suggestion_output_parser import parse_suggestion
from app.llm_support.chain_educational_level_parser import parse_educational_level_input
from app.llm_support.chain_manager import execute_chain
from app.llm_support.chain_output_parser import parse_chain_output
from app.metadatabuilder.build_full_metadata import build_metadata
from app.metadatabuilder.build_optional_metadata import build_optional_metadata
from app.translator.translator import translate


def generate_full_suggestion(raw_data: dict) -> dict:
    """
    Generates the suggestions for the teaches, educationalAlignment, keywords and educationalLevel
    attribute according to the MOOChub supported frameworks. The title and description are translated
    into English if the input language is detected as German. Suggestions will be generated for all
    attributes present as a keys in the raw_data dictionary. All raw suggestions are parsed into a
    form that can be processed with the metadata_builder module.

    :param raw_data: The raw data containing metadata_builder compatible data and the key-value pairs
    for the suggestions.
    :type raw_data: dict
    :return: Metadata in the MOOChub format including all requested suggestions.
    :rtype: dict
    """
    query = f"{raw_data['name']}. {raw_data['description']}"
    query = translate(query)

    if "teaches" in raw_data.keys():
        teaches_framework = raw_data["teaches"]
        teaches = search_frameworks(teaches_framework, query)

        if teaches:
            teaches = parse_suggestion(teaches)
            raw_data["teaches"] = teaches

    if "educationalAlignment" in raw_data.keys():
        ed_align_framework = raw_data["educationalAlignment"]
        ed_align = search_frameworks(ed_align_framework, query)

        if ed_align:
            ed_align = parse_suggestion(ed_align)
            raw_data["educationalAlignment"] = ed_align

    if "keywords" in raw_data.keys() or "educationalLevel" in raw_data.keys():
        ed_level_framework = parse_educational_level_input(raw_data)
        llm_suggestion = execute_chain(ed_level_framework, query)
        if llm_suggestion:
            llm_suggestion = parse_chain_output(llm_suggestion, ed_level_framework)

            if "keywords" in raw_data.keys():
                raw_data["keywords"] = llm_suggestion["keywords"]
            if "educationalLevel" in raw_data.keys():
                raw_data["educationalLevel"] = llm_suggestion["educationalLevel"]

    return build_metadata(raw_data)


def generate_optional_suggestions(raw_data):
    """
    Generates only the optional attributes keywords, educationalAlignment, teaches
    and educationalLevel. The basis are the title and the description of a course.
    Suggestions are generated according to this information. The data is returned in
    the MOOChub format.

    :param raw_data: The title and the description of a course.
    :type raw_data: dict
    :return: Metadata for the four optional attributes in the MOOChub format.
    :rtype: dict
    """
    output_data = dict()

    query = f"{raw_data['name']}. {raw_data['description']}"
    query = translate(query)

    teaches = search_frameworks([{"educationalFramework": "ESCO"}], query)
    teaches = parse_suggestion(teaches)

    ed_align = search_frameworks([{"educationalFramework": "ISCED-F"}], query)
    ed_align = parse_suggestion(ed_align)

    llm_suggestion = execute_chain("DigComp", query)
    llm_suggestion = parse_chain_output(llm_suggestion, "DigComp")

    output_data["teaches"] = teaches
    output_data["educationalAlignment"] = ed_align
    output_data["educationalLevel"] = llm_suggestion["educationalLevel"]
    output_data["keywords"] = llm_suggestion["keywords"]

    return build_optional_metadata(output_data)
