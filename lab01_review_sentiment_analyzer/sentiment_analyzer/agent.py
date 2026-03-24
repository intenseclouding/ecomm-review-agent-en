import json
import logging

from strands import Agent

# Configure the root strands logger
logging.getLogger("strands").setLevel(logging.INFO)

# Add a handler to see the logs
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()]
)

SYSTEM_PROMPT = """
    You are a review sentiment analysis expert.
    Please analyze the review text, classify the sentiment, and assign a score.

    <sentiment_classification>
    - positive: Positive sentiment (satisfaction, joy, recommendation, etc.)
    - negative: Negative sentiment (dissatisfaction, disappointment, not recommended, etc.)
    - neutral: Neutral sentiment (objective description, simple information, etc.)
    </sentiment_classification>

    <score_range>
    Sentiment score: -1.0 (very negative) ~ 1.0 (very positive)
    </score_range>

    <guidelines>
    - Carefully detect irony and sarcastic expressions (e.g., 'really great' + negative context)
    - If there are mixed sentiments, identify the overall dominant sentiment
    - Consider Korean euphemistic expressions: 'not bad' is positive, 'so-so' is moderate satisfaction
    - Understand the context of domain-specific terminology (e.g., 'difficult' in gaming can be positive)
    - Consider the relative meaning of comparative expressions (e.g., 'better than ~')
    - Set confidence low if the text is too short or ambiguous
    </guidelines>

    <output_format>
    Please return the result in JSON format. Do not include backticks or code block formatting (```json, ```python, etc.) in your response:
    {
    "sentiment": "positive|negative|neutral",
    "score": 0.8,
    "confidence": 0.9,
    "reason": "Analysis rationale"
    }
    </output_format>
"""
# Create sentiment analysis Agent


def analyze_sentiment(review_content: str) -> dict:
    """
    Main function to analyze the sentiment of review text (using Strands Agent)

    Args:
        review_content (str): Review text to analyze

    Returns:
        dict: Sentiment analysis result
    """
    sentiment_agent = Agent(
        model="us.anthropic.claude-sonnet-4-20250514-v1:0",
        system_prompt=SYSTEM_PROMPT,
    )

    # Call Strands Agent
    result = sentiment_agent(review_content)
    str_result = str(result)

    return {
        "success": True,
        "sentiment_result": json.loads(str_result),
        "raw_response": str_result,
    }
