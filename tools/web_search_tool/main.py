import sys
import os


project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

from tools.web_search_tool.util import (
    extract_relevance_url,
    generate_search_keywords,
    search_non_visual,
    search_visual,
)

from engine.tool_framework.tool_runner import ToolRunner
from engine.tool_framework import simple_tool


@simple_tool("Web Search Tool")
def web_search(intent: str):
    """
    This tool is used to search the web for information.
    Args:
        intent (str): The intent of the user.
    Returns:
        A list of URLs that match the intent.
    """

    # Generate search keywords
    keywords = generate_search_keywords(intent)

    # Perform web search
    is_visual = os.getenv("VISUAL")
    if is_visual == "T":
        content_list = search_visual(keywords)
    else:
        content_list = search_non_visual(keywords)

    if not content_list:
        return "No results found."
    else:
        # Extract relevance URLs
        contents = " ".join(content_list)
        relevance_urls = extract_relevance_url(intent, contents)
        if not relevance_urls:
            return "No results found."
        return relevance_urls


def main():
    tool = web_search()
    runner = ToolRunner(tool)
    runner.run()


if __name__ == "__main__":
    main()
