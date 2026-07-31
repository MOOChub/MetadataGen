# general
from app.helper.load_config import load_llm_config
from app.llm_support.template_builder import create_template
from langchain_core.output_parsers import StrOutputParser

# Google/Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

# Anthropic/Claude
from langchain_anthropic import ChatAnthropic
import anthropic


def execute_chain(framework: str, query: str) -> str | None:
    """
    Executes a langchain to generate suggestions for keywords and an educational level for a
    given course. A configuration file sets which LLM is to use. The basis for the suggestions
    are the course title and description. If an error occurres, None will be returned.

    :param framework: The framework to be used for the educationalLevel suggestion.
    :type framework: str
    :param query: The name and description of the course.
    :type query: str
    :return: The LLM raw answer ready for parsing.
    :rtype: str
    """
    chats = {
        "GEMINI": ChatGoogleGenerativeAI,
        "CLAUDE": ChatAnthropic
    }
    errors = {
        "GEMINI": ChatGoogleGenerativeAIError,
        "CLAUDE": anthropic.APIError
    }

    model_family = load_llm_config()["ACTIVE"]
    chat = chats[model_family]
    llm_error = errors[model_family]

    prompt_template = create_template(framework)

    model_name = load_llm_config()[model_family]

    try:
        model = chat(model=model_name, temperature=0)

        chain = prompt_template | model | StrOutputParser()

        return chain.invoke({"query": query})
    except TypeError as e:
        print(e)
        print("Most likely an error with the authentication. "
              "Please, check the detailed error message above! "
              "Skipping keywords and educational level suggestion...")
    except llm_error as e:
        print(e)
        print("An error occurred during LLM data exchange (s. above)! "
              "Skipping keywords and educational level suggestion...")
        return None
