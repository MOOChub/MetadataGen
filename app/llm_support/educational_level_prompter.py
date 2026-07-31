from app.framework_handler.framework_data_retriever import get_full_framework


PROMPT = 'Please give a rating for the difficulty of a learning resource based on the title and the ' \
            'description. Please use the given framework under level_framework and assign ' \
            'the appropriate name. The name is found in the "name" column. ' \
            'Please select the appropriate name according to the "explanation"' \
            'column. Return the results in this form:' \
            '"educationalLevel = <the name you picked according to the framework>".\n'


def get_prompt(framework: str) -> str:
    """
    Provides the prompt the educationalLevel attribute suggestion. It will add a set of predefined
    terms to the prompt based on the specified framework.

    :param framework: The framework from which the educational level has to be selected.
    :type framework: str
    :return: A prompt for generating the suggestion including the vocabulary that shall be used.
    :rtype: str
    """
    full_framework = get_full_framework("educationalLevel", framework)
    framework = full_framework[["name", "uri", "description"]]
    return f"{PROMPT}\n" \
           f"level_framework: {framework}\n\n"
