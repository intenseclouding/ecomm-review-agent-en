import json
import logging
from dataclasses import dataclass
from string import Template
from typing import List, Literal

from pydantic import BaseModel, Field
from strands import Agent, tool
from strands_tools import file_read

# Configure the root strands logger
logging.getLogger("strands").setLevel(logging.INFO)

# Add a handler to see the logs
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()]
)


SYSTEM_PROMPT = """
You are a keyword-based review analysis expert.

<core_tasks>
- Accurately extract sentences related to keywords from the review text, considering linguistic characteristics and context
- Perform precise matching with registered keywords
</core_tasks>

<workflow>
1. Retrieve registered keywords: Use the file_read tool to read the "registered_keywords.txt" file and obtain the registered keyword list
2. Analyze review text: Refer to the registered keywords to identify related keywords and phrases in the review
3. Perform matching:
   - Prioritize exact matches
   - Consider partial matches and synonyms
   - Consider semantic synonyms
</workflow>

<output_format>
Include the following values in the result:
{
  "matched_keywords": [
        {
            "keyword": "Matched keyword",
            "match_type": "exact|partial|semantic",
            "original_phrase": "Original phrase found in review (exact text extracted from the review)"
        }
    ]
}

Note: original_phrase must be the exact text contained in the original review.
</output_format>

<guidelines>
- Consider linguistic characteristics (particles, verb conjugations) when matching
- Include keywords used in negative sentences but process them separately
- Remove duplicate keywords and keep only the best matches
</guidelines>
"""

KEYWORD_EXTRACTOR_PROMPT_TEMPLATE = Template(
    """
Find content matching registered keywords in the review below.
<review>
    $review_text
</review>
"""
)


class KeywordHighlight(BaseModel):
    """Dataset of matched sentences per keyword"""

    keyword: str = Field(description="Reference keyword")
    match_type: Literal["exact", "partial", "semantic"]
    original_phrase: str = Field(description="Original phrase found in review")


class KeywordAnalysisResult(BaseModel):
    """Class containing keyword analysis results"""

    matched_keywords: List[KeywordHighlight]


@tool
def search_keywords(review_text: str) -> dict:
    """
    Function to search for sentences matching keywords in a review

    Args:
        review_text (str): Review text

    Returns:
        dict: Keyword analysis result
    """

    logging.info(f"search_keywords called with review_text: {review_text}")

    # Keyword matching Agent
    keyword_agent = Agent(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        tools=[file_read],
        callback_handler=None,
        system_prompt=SYSTEM_PROMPT,
    )

    # Run Agent
    prompt = KEYWORD_EXTRACTOR_PROMPT_TEMPLATE.substitute(review_text=review_text)
    agent_response = keyword_agent(prompt)
    str_response = str(agent_response)

    # Output as structured output
    result = keyword_agent.structured_output(
        KeywordAnalysisResult, "Extract the keyword analysis results in a structured format"
    )

    return {
        "success": True,
        "analysis_result": (
            result.model_dump() if hasattr(result, "model_dump") else result.__dict__
        ),
        "raw_response": str_response,
    }
