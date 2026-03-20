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

    To generate an appropriate seller response to a customer review, follow these steps exactly:

    <workflow>
    1. You must first use the retrieve tool to search the knowledge base for relevant information
    2. Analyze the customer review to identify the customer's concerns or sentiments
    3. Prepare an accurate response using the retrieved information
    4. Apply the seller's tone and style as defined in SELLER_ANSWER_PROMPT
    5. Generate a natural and helpful response as if the seller is replying directly
    </workflow>

    <response_guidelines>
    - All factual information should be based on the retrieved knowledge base content
    - Match the seller's communication style (a seller in their 40s responding to customers in their 30s)
    - Provide specific and actionable responses rather than vague answers
    - Maintain a professional yet warm tone
    - Do not publicly mention personal or sensitive information
    - Direct complex issues to customer service as appropriate
    - Do not use backticks or code block formatting (```json, ```python, etc.) in the response. Show it as plain text.

    </response_guidelines>

    <review_type_responses>
    Positive review: Express gratitude + promise of continued service
    Negative review: Sincere apology + specific resolution + relevant policy information
    Inquiry review: Provide accurate information + guide to additional inquiry channels
    Shipping related: Refer to shipping guide information
    Refund/Exchange: Refer to refund guide policy
    </review_type_responses>

    <mandatory_rules>
    - You must use the retrieve tool before generating a response
    - You must follow the tone guide in SELLER_ANSWER_PROMPT
    - Write naturally as if the seller is responding directly
    - Never fabricate information that was not found in the knowledge base
    - Responses should be concise yet complete
    </mandatory_rules>

    Remember: You represent the seller, so respond authentically as a seller, using the knowledge base as the source of truth.
"""

SELLER_ANSWER_PROMPT = """
I am a seller in my 40s, and our products are mainly used by customers in their 30s, so responses should be tailored accordingly.
Please provide clean and calm information-based responses so there is no room for misunderstanding.
The tone must be polite.
"""


def generate_auto_response(review: str) -> Dict[str, Any]:
    """
    Main function to generate an automatic response to a review

    Args:
        review (str): The review text to analyze

    Returns:
        Dict[str, Any]: The auto response result
    """

    # Create a new Agent for each request
    auto_response_agent = Agent(
        tools=[retrieve],
        system_prompt=RESPONSE_SYSTEM_PROMPT
        + f"""
        SELLER_ANSWER_PROMPT: {SELLER_ANSWER_PROMPT}
        """,
    )

    # Generate auto response for the review
    response = auto_response_agent(review)

    # Extract tool_result
    tool_results = filter_tool_result(auto_response_agent)

    # Return result - including tool_results
    result = {"response": str(response), "tool_results": tool_results}
    return result


def filter_tool_result(agent: Agent) -> List:
    """
    Function to extract only tool_result from the Agent's execution results

    Args:
        agent (Agent): The Agent instance

    Returns:
        Dict[str, Any]: A dictionary containing only tool_result
    """
    tool_results = []
    for m in agent.messages:
        for content in m["content"]:
            if "toolResult" in content:
                tool_results.append(m["content"][0]["toolResult"])
    return tool_results
