import json
import logging
import os
from typing import Any, Dict, List

from strands import Agent, tool
from strands_tools import retrieve

# Configure the root strands logger
logging.getLogger("strands").setLevel(logging.INFO)

# Add a handler to see the logs
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()]
)

# export KNOWLEDGE_BASE_ID=your_kb_id
# export AWS_REGION=us-west-2
os.environ["KNOWLEDGE_BASE_ID"] = "your_kb_id"
os.environ["AWS_REGION"] = "us-west-2"

RESPONSE_SYSTEM_PROMPT = """
    You are an AI assistant that automatically responds to customer reviews on behalf of an e-commerce seller.

    To generate appropriate seller responses to customer reviews, please follow the steps below exactly:

    <workflow>
    1. You must first use the retrieve tool to search for relevant information from the knowledge base
    2. Analyze the customer review to identify the customer's concerns or emotions
    3. Prepare an accurate response using the retrieved information
    4. Apply the seller's tone and style defined in SELLER_ANSWER_PROMPT
    5. Generate a natural and helpful response as if the seller is directly replying
    </workflow>

    <response_guidelines>
    - All factual information should be based on the retrieved knowledge base content
    - Match the seller's communication style (a seller in their 40s responding to customers in their 30s)
    - Provide specific and actionable responses rather than vague answers
    - Maintain a professional yet warm tone
    - Do not publicly mention personal or sensitive information
    - Appropriately direct complex issues to customer service
    - Do not add backticks or code block formatting (```json, ```python, etc.) to the response. Please show as plain text.

    </response_guidelines>

    <review_type_responses>
    Positive review: Thank you message + promise of continued service
    Negative review: Sincere apology + specific resolution + relevant policy guidance
    Inquiry review: Accurate information + additional inquiry channel guidance
    Shipping related: Refer to shipping guide information
    Refund/Exchange: Refer to refund guide policy
    </review_type_responses>

    <mandatory_rules>
    - You must use the retrieve tool before responding
    - You must follow the tone guide in SELLER_ANSWER_PROMPT
    - Write naturally in Korean as if the seller is directly responding
    - Never fabricate information not found in the knowledge base
    - Responses should be concise but complete
    </mandatory_rules>

    Remember: You represent the seller, so respond authentically as a seller using the knowledge base as the source of truth.
"""

SELLER_ANSWER_PROMPT = """
I am a seller in my 40s, and our products are mainly used by people in their 30s, so responses should take this into account.
Please provide clean, calm, and information-based responses to avoid any misunderstanding with customers.
However, the tone must be polite.
"""


@tool
def generate_auto_response(review: str, sentiment: str) -> Dict[str, Any]:
    """
    Main function to generate an automatic response to a review

    Args:
        review (str): Review text to analyze
        sentiment (str): Sentiment state of the review

    Returns:
        Dict[str, Any]: Auto response result
    """

    # Create a new Agent for each request
    auto_response_agent = Agent(
        tools=[retrieve],
        callback_handler=None,
        system_prompt=RESPONSE_SYSTEM_PROMPT
        + f"""
        SELLER_ANSWER_PROMPT: {SELLER_ANSWER_PROMPT}
        """,
    )

    # Generate auto response for the review
    response = auto_response_agent(
        f"Please generate a reply reflecting the following review and sentiment. <review>{review}</review><sentiment>{sentiment}</sentiment>"
    )

    # Extract tool_result
    tool_results = filter_tool_result(auto_response_agent)

    # Return result - including tool_results
    result = {"response": str(response), "tool_results": tool_results}
    return result


def filter_tool_result(agent: Agent) -> List:
    """
    Function to extract only tool_result from the Agent's execution results

    Args:
        agent (Agent): Agent instance

    Returns:
        Dict[str, Any]: Dictionary containing only tool_results
    """
    tool_results = []
    for m in agent.messages:
        for content in m["content"]:
            if "toolResult" in content:
                tool_results.append(m["content"][0]["toolResult"])
    return tool_results
