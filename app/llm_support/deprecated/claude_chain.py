from langchain_anthropic import ChatAnthropic
from app.llm_support.template_builder import create_template
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from app.helper.load_config import load_llm_config


def execute_chain(query: str, framework: str) -> str | None:
    """
    Executes a langchain to generate suggestions for keywords and an educational level
    of a given course. The basis for the suggestion are the course title and description.
    This is the integration for Anthropic's Claude models.

    :param query: The title and the description of the course combined into a single string.
    :type query: str
    :param framework: The framework for which the educational level suggestion is made.
    :type framework: str
    :return: The suggested educational level and keywords for the course.
    :rtype: str
    """
    prompt_template = create_template(framework)

    model_name = load_llm_config()["CLAUDE"]
    try:
        model = ChatAnthropic(model=model_name, temperature=0)

        chain = prompt_template | model | StrOutputParser()

        return chain.invoke({"query": query})
    except ChatGoogleGenerativeAIError as e:
        print(e)
        print("Invalid API key! Skipping keywords and educational level suggestion...")
        return None
